from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from . import views

urlpatterns = [
    # Auth
    path('auth/register/', views.register_user, name='register'),
    path('auth/login/', views.login_user, name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    
    # Buses
    path('buses/find/', views.find_bus, name='find_bus'),
    
    # Bookings
    path('bookings/', views.list_bookings, name='list_bookings'),
    path('bookings/create/', views.create_booking, name='create_booking'),
    path('bookings/<int:pk>/cancel/', views.cancel_booking, name='cancel_booking'),
]
