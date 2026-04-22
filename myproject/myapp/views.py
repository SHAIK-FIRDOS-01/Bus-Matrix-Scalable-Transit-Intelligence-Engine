from django.shortcuts import render
from decimal import Decimal

# Create your views here.
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from .models import User, Bus, Book
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .forms import UserLoginForm, UserRegisterForm
from django.contrib.auth.decorators import login_required
from decimal import Decimal
from django.db import transaction


def home(request):
    if request.user.is_authenticated:
        import datetime
        upcoming_buses = Bus.objects.filter(date__gte=datetime.date.today()).order_by('date', 'time')[:10]
        return render(request, 'myapp/home.html', {'upcoming_buses': upcoming_buses})
    else:
        return render(request, 'myapp/signin.html')


@login_required(login_url='signin')
def findbus(request):
    context = {}
    if request.method == 'POST':
        source_r = request.POST.get('source', '').strip()
        dest_r = request.POST.get('destination', '').strip()
        date_r = request.POST.get('date')
        
        # Calculate target_date for final booking irrespective of physical bus date
        import datetime
        target_date = date_r if date_r else str(datetime.date.today())
        
        # Pull all static matrix topologies natively
        q_all = Bus.objects.all()
        bus_list = []
        
        src_lower = source_r.strip().lower()
        dst_lower = dest_r.strip().lower()
        
        for b in q_all:
            if b.route_nodes:
                nodes_data = [n.split(':') for n in b.route_nodes.split(',')]
                node_names = [n[0] for n in nodes_data]
                
                if src_lower in node_names and dst_lower in node_names:
                    idx1 = node_names.index(src_lower)
                    idx2 = node_names.index(dst_lower)
                    if idx1 < idx2:
                        dist1 = float(nodes_data[idx1][1])
                        dist2 = float(nodes_data[idx2][1])
                        segment_dist = dist2 - dist1
                        
                        b.dynamic_price = max(round(segment_dist * 2.50, 2), 50.0) 
                        b.display_source = source_r.title()
                        b.display_dest = dest_r.title()
                        bus_list.append(b)
        
        # Organize purely by sequential shift times
        bus_list.sort(key=lambda x: str(x.time))

        if bus_list:
            return render(request, 'myapp/list.html', locals())
        else:
            context["error"] = "No routes match that combination. Please verify your spelling or try another city."
            return render(request, 'myapp/findbus.html', context)
    else:
        return render(request, 'myapp/findbus.html')


@login_required(login_url='signin')
def bookings(request):
    context = {}
    if request.method == 'POST':
        id_r = request.POST.get('bus_id')
        seats_r = int(request.POST.get('no_seats'))
        
        # Dynamic Subset Routing Interceptors
        override_source = request.POST.get('segment_source')
        override_dest = request.POST.get('segment_dest')
        override_price_str = request.POST.get('segment_price')
        target_date = request.POST.get('target_date')
        
        username_r = request.user.username
        email_r = request.user.email
        userid_r = request.user.id

        try:
            with transaction.atomic():
                bus = Bus.objects.select_for_update().get(id=id_r)
                if bus.rem >= seats_r:
                    # Leverage mathematical subset price if mapped, else raw master price
                    active_price = float(override_price_str) if override_price_str else float(bus.price)
                    
                    cost = seats_r * active_price
                    bus.rem -= seats_r
                    bus.save()
                    
                    final_src = override_source.title() if override_source else bus.source
                    final_dst = override_dest.title() if override_dest else bus.dest
                    
                    book = Book.objects.create(
                        email=email_r, name=username_r, userid=userid_r, busid=id_r,
                        bus_name=bus.bus_name, source=final_src, dest=final_dst,
                        price=active_price, nos=seats_r, date=target_date if target_date else bus.date, time=bus.time, status='B'
                    )
                    return render(request, 'myapp/bookings.html', locals())
                else:
                    context["error"] = "Sorry select fewer number of seats"
                    return render(request, 'myapp/findbus.html', context)
        except Bus.DoesNotExist:
            context["error"] = "Bus not found."
            return render(request, 'myapp/findbus.html', context)
    else:
        return render(request, 'myapp/findbus.html')


@login_required(login_url='signin')
def cancellings(request):
    context = {}
    if request.method == 'POST':
        id_r = request.POST.get('bus_id')
        #seats_r = int(request.POST.get('no_seats'))

        try:
            with transaction.atomic():
                book = Book.objects.select_for_update().get(id=id_r)
                bus = Bus.objects.select_for_update().get(id=book.busid)
                bus.rem += book.nos
                bus.save()
                
                book.status = 'C'
                book.nos = 0
                book.save()
            return redirect(seebookings)
        except Book.DoesNotExist:
            context["error"] = "Sorry You have not booked that bus"
            return render(request, 'myapp/error.html', context)
        except Bus.DoesNotExist:
            context["error"] = "This bus route was retired or no longer exists."
            return render(request, 'myapp/error.html', context)
    else:
        return render(request, 'myapp/findbus.html')


@login_required(login_url='signin')
def seebookings(request,new={}):
    context = {}
    id_r = request.user.id
    book_list = Book.objects.filter(userid=id_r).exclude(status='CANCELLED')
    if book_list:
        return render(request, 'myapp/booklist.html', locals())
    else:
        context["error"] = "You have no active bookings."
        return render(request, 'myapp/findbus.html', context)


def signup(request):
    context = {}
    if request.method == 'POST':
        name_r = request.POST.get('name')
        email_r = request.POST.get('email')
        password_r = request.POST.get('password')
        user = User.objects.create_user(name_r, email_r, password_r, )
        if user:
            login(request, user)
            return render(request, 'myapp/thank.html')
        else:
            context["error"] = "Provide valid credentials"
            return render(request, 'myapp/signup.html', context)
    else:
        return render(request, 'myapp/signup.html', context)


def signin(request):
    context = {}
    if request.method == 'POST':
        name_r = request.POST.get('name')
        password_r = request.POST.get('password')
        user = authenticate(request, username=name_r, password=password_r)
        if user:
            login(request, user)
            # username = request.session['username']
            context["user"] = name_r
            context["id"] = request.user.id
            return render(request, 'myapp/success.html', context)
            # return HttpResponseRedirect('success')
        else:
            context["error"] = "Provide valid credentials"
            return render(request, 'myapp/signin.html', context)
    else:
        context["error"] = "You are not logged in"
        return render(request, 'myapp/signin.html', context)


def signout(request):
    context = {}
    logout(request)
    context['error'] = "You have been logged out"
    return render(request, 'myapp/signin.html', context)


def success(request):
    context = {}
    context['user'] = request.user
    return render(request, 'myapp/success.html', context)
