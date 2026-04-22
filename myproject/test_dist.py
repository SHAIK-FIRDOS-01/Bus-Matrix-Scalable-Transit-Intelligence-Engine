import requests
from geopy.geocoders import Nominatim
import time

def test_distance():
    print("Initializing geocoders...")
    geolocator = Nominatim(user_agent="ts_ap_bus_system_v1")
    
    source = "Hyderabad, Telangana"
    dest = "Vijayawada, Andhra Pradesh"
    
    print(f"Geocoding {source}...")
    l1 = geolocator.geocode(source)
    time.sleep(1.5) # respect rate limits
    print(f"Geocoding {dest}...")
    l2 = geolocator.geocode(dest)
    
    if l1 and l2:
        print(f"Coords: {l1.longitude},{l1.latitude} to {l2.longitude},{l2.latitude}")
        url = f"http://router.project-osrm.org/route/v1/driving/{l1.longitude},{l1.latitude};{l2.longitude},{l2.latitude}?overview=false"
        print("Calling OSRM API...")
        r = requests.get(url).json()
        if r.get('code') == 'Ok':
            dist_km = r['routes'][0]['distance'] / 1000
            print(f"Distance: {dist_km:.2f} km")
            print(f"Estimated fare at Rs 2.5/km: Rs {dist_km * 2.5:.2f}")
        else:
            print("OSRM Failed:", r)
    else:
        print("Geocoding failed.")

if __name__ == '__main__':
    test_distance()
