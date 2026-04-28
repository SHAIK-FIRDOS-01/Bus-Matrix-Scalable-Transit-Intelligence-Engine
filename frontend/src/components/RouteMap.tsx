import React, { useEffect, useState } from 'react';
import { MapContainer, TileLayer, Marker, Popup, Polyline, useMap } from 'react-leaflet';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';

// Fix for default marker icons in React-Leaflet
import markerIcon2x from 'leaflet/dist/images/marker-icon-2x.png';
import markerIcon from 'leaflet/dist/images/marker-icon.png';
import markerShadow from 'leaflet/dist/images/marker-shadow.png';

delete (L.Icon.Default.prototype as any)._getIconUrl;
L.Icon.Default.mergeOptions({
    iconRetinaUrl: markerIcon2x,
    iconUrl: markerIcon,
    shadowUrl: markerShadow,
});

interface RouteMapProps {
  source: string;
  destination: string;
}

const FitBounds: React.FC<{ coords: [number, number][] }> = ({ coords }) => {
  const map = useMap();
  useEffect(() => {
    if (coords.length > 1) {
      const bounds = L.polyline(coords).getBounds();
      map.fitBounds(bounds, { padding: [50, 50] });
    }
  }, [coords, map]);
  return null;
};

const RouteMap: React.FC<RouteMapProps> = ({ source, destination }) => {
  const [route, setRoute] = useState<[number, number][]>([]);
  const [markers, setMarkers] = useState<{ pos: [number, number], label: string }[]>([]);
  const [distance, setDistance] = useState<string>('Calculating...');
  const [duration, setDuration] = useState<string>('Calculating...');

  useEffect(() => {
    const fetchRouteData = async () => {
      try {
        // 1. Geocode cities
        const geocode = async (city: string) => {
          const res = await fetch(`https://nominatim.openstreetmap.org/search?format=json&q=${city}, India`);
          const data = await res.json();
          if (data && data.length > 0) return [parseFloat(data[0].lat), parseFloat(data[0].lon)] as [number, number];
          return null;
        };

        const srcCoords = await geocode(source);
        const dstCoords = await geocode(destination);

        if (srcCoords && dstCoords) {
          setMarkers([
            { pos: srcCoords, label: `Departure: ${source}` },
            { pos: dstCoords, label: `Arrival: ${destination}` }
          ]);

          // 2. Fetch OSRM route
          const osrmRes = await fetch(`https://router.project-osrm.org/route/v1/driving/${srcCoords[1]},${srcCoords[0]};${dstCoords[1]},${dstCoords[0]}?overview=full&geometries=geojson`);
          const osrmData = await osrmRes.json();

          if (osrmData.code === 'Ok') {
            const path = osrmData.routes[0].geometry.coordinates.map((c: any) => [c[1], c[0]] as [number, number]);
            setRoute(path);
            setDistance((osrmData.routes[0].distance / 1000).toFixed(1) + ' km');
            const hrs = Math.floor(osrmData.routes[0].duration / 3600);
            const mins = Math.floor((osrmData.routes[0].duration % 3600) / 60);
            setDuration(`${hrs}h ${mins}m`);
          }
        }
      } catch (error) {
        console.error('Map loading error:', error);
      }
    };

    fetchRouteData();
  }, [source, destination]);

  return (
    <div className="glass-card overflow-hidden">
      <div className="h-[400px] w-full">
        <MapContainer center={[17.3850, 78.4867]} zoom={6} className="h-full w-full">
          <TileLayer
            url="https://{s}.basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}{r}.png"
            attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>'
          />
          {markers.map((m, i) => (
            <Marker key={i} position={m.pos}>
              <Popup>{m.label}</Popup>
            </Marker>
          ))}
          {route.length > 0 && (
            <>
              <Polyline positions={route} pathOptions={{ color: '#2563eb', weight: 4, opacity: 0.7 }} />
              <FitBounds coords={route} />
            </>
          )}
        </MapContainer>
      </div>
      <div className="p-6 bg-slate-50 border-t border-slate-100 flex justify-between items-center">
        <div>
          <p className="text-xs font-bold text-slate-400 uppercase tracking-widest mb-1">Highway Distance</p>
          <p className="text-xl font-black text-slate-900">{distance}</p>
        </div>
        <div className="text-right">
          <p className="text-xs font-bold text-slate-400 uppercase tracking-widest mb-1">Estimated Time</p>
          <p className="text-xl font-black text-slate-900">{duration}</p>
        </div>
      </div>
    </div>
  );
};

export default RouteMap;
