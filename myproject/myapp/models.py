from django.db import models
from geopy.geocoders import Nominatim
import requests
from datetime import datetime, timedelta

class Bus(models.Model):
    bus_name = models.CharField(max_length=30)
    source = models.CharField(max_length=30)
    dest = models.CharField(max_length=30)
    nos = models.PositiveIntegerField()
    rem = models.PositiveIntegerField()
    price = models.DecimalField(decimal_places=2, max_digits=6)
    date = models.DateField()
    time = models.TimeField()
    distance_km = models.FloatField(null=True, blank=True)
    travel_time_hrs = models.FloatField(null=True, blank=True)
    source_lat = models.FloatField(null=True, blank=True)
    source_lon = models.FloatField(null=True, blank=True)
    dest_lat = models.FloatField(null=True, blank=True)
    dest_lon = models.FloatField(null=True, blank=True)
    route_nodes = models.TextField(default="", blank=True)

    def save(self, *args, **kwargs):
        if not self.distance_km:
            try:
                geolocator = Nominatim(user_agent="bus_reserve_ts_ap")
                # Attempt to geocode assuming TS/AP contextual framing
                l1 = geolocator.geocode(self.source + ", India")
                l2 = geolocator.geocode(self.dest + ", India")
                
                if l1 and l2:
                    self.source_lat = l1.latitude
                    self.source_lon = l1.longitude
                    self.dest_lat = l2.latitude
                    self.dest_lon = l2.longitude
                    
                    url = f"http://router.project-osrm.org/route/v1/driving/{l1.longitude},{l1.latitude};{l2.longitude},{l2.latitude}?overview=false"
                    r = requests.get(url, timeout=5).json()
                    if r.get('code') == 'Ok':
                        dist_km = r['routes'][0]['distance'] / 1000.0
                        self.distance_km = round(dist_km, 2)
                        
                        base_hrs = dist_km / 100.0
                        if dist_km > 200:
                            base_hrs += 2.5
                        elif dist_km > 150:
                            base_hrs += 1.0
                            
                        self.travel_time_hrs = round(base_hrs, 2)
                        self.price = round(dist_km * 2.50, 2) # 2.50 Rs per km dynamic base fare
            except Exception as e:
                print("Error computing route API:", e)
        super().save(*args, **kwargs)

    @property
    def arrival_datetime(self):
        if self.date and self.time and self.travel_time_hrs:
            dt = datetime.combine(self.date, self.time)
            return dt + timedelta(hours=self.travel_time_hrs)
        return None

    @property
    def arrival_time_str(self):
        arr = self.arrival_datetime
        if arr:
            return arr.strftime("%I:%M %p").lstrip('0')
        return "N/A"

    def __str__(self):
        return self.bus_name


class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    email = models.EmailField()
    name = models.CharField(max_length=30)
    password = models.CharField(max_length=30)

    def __str__(self):
        return self.email


class Book(models.Model):
    BOOKED = 'B'
    CANCELLED = 'C'

    TICKET_STATUSES = ((BOOKED, 'Booked'),
                       (CANCELLED, 'Cancelled'),)
    email = models.EmailField()
    name = models.CharField(max_length=30)
    userid = models.PositiveIntegerField()
    busid = models.PositiveIntegerField()
    bus_name = models.CharField(max_length=30)
    source = models.CharField(max_length=30)
    dest = models.CharField(max_length=30)
    nos = models.PositiveIntegerField()
    price = models.DecimalField(decimal_places=2, max_digits=6)
    date = models.DateField()
    time = models.TimeField()
    status = models.CharField(choices=TICKET_STATUSES, default=BOOKED, max_length=2)

    def __str__(self):
        return self.email
