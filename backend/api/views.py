from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework import status, generics, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
import datetime

from .models import Bus, Book
from .serializers import UserSerializer, BusSerializer, BookSerializer

def calculate_segment_price(bus, source_name, dest_name):
    """Securely calculate price for a segment on the server side."""
    if not bus.route_nodes:
        # Fallback for buses without explicit node data (only if exact source/dest match)
        if bus.source.lower() == source_name.lower() and bus.dest.lower() == dest_name.lower():
            return float(bus.price)
        return 0
        
    nodes_data = [n.split(':') for n in bus.route_nodes.split(',')]
    node_names = [n[0].lower() for n in nodes_data]
    
    s_name = source_name.lower()
    d_name = dest_name.lower()
    
    if s_name in node_names and d_name in node_names:
        idx1 = node_names.index(s_name)
        idx2 = node_names.index(d_name)
        if idx1 < idx2:
            dist1 = float(nodes_data[idx1][1])
            dist2 = float(nodes_data[idx2][1])
            segment_dist = dist2 - dist1
            return max(round(segment_dist * 2.50, 2), 50.0)
            
    return 0

# --- Authentication Views ---

@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def register_user(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        return Response({
            'user': serializer.data,
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def login_user(request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(username=username, password=password)
    if user:
        refresh = RefreshToken.for_user(user)
        return Response({
            'user': UserSerializer(user).data,
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        })
    return Response({'error': 'Invalid Credentials'}, status=status.HTTP_401_UNAUTHORIZED)

# --- Bus Views ---

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def find_bus(request):
    source_r = request.query_params.get('source', '').strip().lower()
    dest_r = request.query_params.get('destination', '').strip().lower()
    date_r = request.query_params.get('date')
    
    if not source_r or not dest_r:
        return Response({'error': 'Source and destination are required'}, status=status.HTTP_400_BAD_REQUEST)

    target_date = date_r if date_r else str(datetime.date.today())
    q_all = Bus.objects.all()
    bus_list = []
    
    for b in q_all:
        if b.route_nodes:
            price = calculate_segment_price(b, source_r, dest_r)
            if price > 0: # Check if route exists for this bus
                data = BusSerializer(b).data
                data['dynamic_price'] = price
                data['target_date'] = target_date
                data['display_source'] = source_r.title()
                data['display_dest'] = dest_r.title()
                bus_list.append(data)
    
    bus_list.sort(key=lambda x: str(x['time']))
    return Response(bus_list)

# --- Booking Views ---

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def create_booking(request):
    bus_id = request.data.get('bus_id')
    seats_r = int(request.data.get('no_seats', 1))
    
    # Optional overrides for sub-segment routing
    override_source = request.data.get('segment_source')
    override_dest = request.data.get('segment_dest')
    override_price = request.data.get('segment_price')
    target_date = request.data.get('target_date')

    try:
        with transaction.atomic():
            bus = Bus.objects.select_for_update().get(id=bus_id)
            
            # Security: Recalculate price on server side
            if override_source and override_dest:
                unit_price = calculate_segment_price(bus, override_source, override_dest)
            else:
                unit_price = float(bus.price)
                
            total_price = round(unit_price * seats_r, 2)

            if bus.rem >= seats_r:
                bus.rem -= seats_r
                bus.save()
                
                final_src = override_source.title() if override_source else bus.source
                final_dst = override_dest.title() if override_dest else bus.dest
                
                book = Book.objects.create(
                    user=request.user,
                    bus=bus,
                    bus_name=bus.bus_name,
                    source=final_src,
                    dest=final_dst,
                    price=total_price, # Store total price for the transaction
                    nos=seats_r,
                    date=target_date if target_date else bus.date,
                    time=bus.time,
                    status=Book.BOOKED
                )
                return Response(BookSerializer(book).data, status=status.HTTP_201_CREATED)
            else:
                return Response({'error': 'Not enough seats available'}, status=status.HTTP_400_BAD_REQUEST)
    except Bus.DoesNotExist:
        return Response({'error': 'Bus not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def list_bookings(request):
    bookings = Book.objects.filter(user=request.user).exclude(status=Book.CANCELLED)
    serializer = BookSerializer(bookings, many=True)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def cancel_booking(request, pk):
    try:
        with transaction.atomic():
            book = Book.objects.select_for_update().get(id=pk, user=request.user)
            if book.status == Book.CANCELLED:
                return Response({'error': 'Already cancelled'}, status=status.HTTP_400_BAD_REQUEST)
                
            bus = Bus.objects.select_for_update().get(id=book.bus.id)
            bus.rem += book.nos
            bus.save()
            
            book.status = Book.CANCELLED
            # We don't set nos to 0 here to keep record of how many were booked originally
            # But the user logic might expect it. Let's keep it 0 as per previous logic.
            book.nos = 0 
            book.save()
            
            return Response({'message': 'Booking cancelled successfully'})
    except Book.DoesNotExist:
        return Response({'error': 'Booking not found or unauthorized'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
