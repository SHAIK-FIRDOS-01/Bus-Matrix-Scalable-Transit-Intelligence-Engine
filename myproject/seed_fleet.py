import os
import django
from datetime import datetime, timedelta, time
import random

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

from myapp.models import Bus, Book

def clear_existing():
    Bus.objects.all().delete()
    Book.objects.all().delete()
    print("Database cleared of existing buses and legacy tickets.")

def seed():
    corridors = [
        # 1. Coastal Artery
        [("visakhapatnam", 0), ("rajahmundry", 190), ("eluru", 290), ("vijayawada", 360), ("guntur", 400), ("ongole", 530), ("nellore", 650), ("tirupati", 790)],
        # 2. Rayalaseema Express
        [("hyderabad", 0), ("mahabubnagar", 100), ("kurnool", 215), ("anantapur", 360), ("kadapa", 525), ("tirupati", 665)],
        # 3. Central Cross-State
        [("hyderabad", 0), ("suryapet", 130), ("khammam", 195), ("vijayawada", 315), ("machilipatnam", 385)],
        # 4. Godavari Belt
        [("hyderabad", 0), ("warangal", 145), ("kothagudem", 285), ("bhadrachalam", 325)],
        # 5. Northern Telangana
        [("hyderabad", 0), ("siddipet", 100), ("karimnagar", 165), ("ramagundam", 225), ("mancherial", 255)]
    ]

    tomorrow = (datetime.now() + timedelta(days=1)).date()
    staggered_slots = [("A", time(8, 0)), ("B", time(14, 0)), ("C", time(20, 0))]

    created = 0
    
    # Process both Forward and Backward iterations dynamically
    for c in corridors:
        # Forward Pathing
        fwd_str = ",".join([f"{n[0]}:{n[1]}" for n in c])
        f_src = c[0][0].title()
        f_dst = c[-1][0].title()
        f_dist = float(c[-1][1])
        
        # Backward Pathing
        max_d = c[-1][1]
        back_nodes = [(n[0], max_d - n[1]) for n in reversed(c)]
        bwd_str = ",".join([f"{n[0]}:{n[1]}" for n in back_nodes])
        b_src = back_nodes[0][0].title()
        b_dst = back_nodes[-1][0].title()
        
        for suffix, depart_time in staggered_slots:
            # Save Forward Routes
            Bus.objects.create(
                bus_name=f"{f_dst}-{suffix}", source=f_src, dest=f_dst, nos=40, rem=40,
                price=round(f_dist * 2.50, 2), date=tomorrow, time=depart_time,
                distance_km=f_dist, travel_time_hrs=round((f_dist/100)+1, 2), route_nodes=fwd_str
            )
            # Save Backward Routes
            Bus.objects.create(
                bus_name=f"{b_dst}-{suffix}", source=b_src, dest=b_dst, nos=40, rem=40,
                price=round(f_dist * 2.50, 2), date=tomorrow, time=depart_time,
                distance_km=f_dist, travel_time_hrs=round((f_dist/100)+1, 2), route_nodes=bwd_str
            )
            created += 2
            
    print(f"Successfully generated Regional Transit Matrix: {created} permanent corridors active.")


if __name__ == '__main__':
    clear_existing()
    seed()
