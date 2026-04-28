import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Search, Map as MapIcon, List as ListIcon, Calendar, Navigation, CheckCircle } from 'lucide-react';
import api from '../services/api';
import type { Bus } from '../types';

import BusCard from '../components/BusCard';
import RouteMap from '../components/RouteMap';

const cities = [
  "Visakhapatnam", "Rajahmundry", "Eluru", "Vijayawada", "Guntur", "Ongole", "Nellore", "Tirupati",
  "Hyderabad", "Mahabubnagar", "Kurnool", "Anantapur", "Kadapa", "Suryapet", "Khammam", "Machilipatnam",
  "Warangal", "Kothagudem", "Bhadrachalam", "Siddipet", "Karimnagar", "Ramagundam", "Mancherial"
];

const FindBus: React.FC = () => {
  const navigate = useNavigate();
  const [source, setSource] = useState('');
  const [dest, setDest] = useState('');
  const [date, setDate] = useState(new Date().toISOString().split('T')[0]);
  const [buses, setBuses] = useState<Bus[]>([]);
  const [loading, setLoading] = useState(false);
  const [bookingId, setBookingId] = useState<number | null>(null);
  const [error, setError] = useState('');

  const handleSearch = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    setBookingId(null);
    try {
      const res = await api.get(`buses/find/?source=${source}&destination=${dest}&date=${date}`);
      setBuses(res.data);
      if (res.data.length === 0) setError('No buses found for this route.');
    } catch (err: any) {
      setError(err.response?.data?.error || 'Something went wrong');
    } finally {
      setLoading(false);
    }
  };

  const handleBooking = async (bus: Bus, selectedSeats: number) => {
    setLoading(true);
    setError('');
    try {
      const basePrice = parseFloat(bus.dynamic_price?.toString() || bus.price.toString());
      const payload = {
        bus_id: bus.id,
        no_seats: selectedSeats,
        segment_source: bus.display_source,
        segment_dest: bus.display_dest,
        segment_price: (basePrice * selectedSeats).toFixed(2),
        target_date: bus.target_date
      };
      await api.post('bookings/create/', payload);
      setBookingId(bus.id);
      setTimeout(() => navigate('/bookings'), 1500);
    } catch (err: any) {
      setError(err.response?.data?.error || 'Booking failed. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="pt-24 pb-12 px-4 max-w-7xl mx-auto space-y-8">
      {/* Search Header */}
      <div className="glass-card p-8 space-y-6">
        <div className="flex items-center gap-3">
          <div className="p-2 bg-brand-100 text-brand-600 rounded-lg">
            <Search className="w-5 h-5" />
          </div>
          <h2 className="text-2xl font-black text-slate-900 tracking-tight">Search Corridors</h2>
        </div>
        
        <form onSubmit={handleSearch} className="grid grid-cols-1 md:grid-cols-4 gap-4 items-end">
          <div className="space-y-1.5">
            <label className="text-xs font-bold text-slate-500 uppercase tracking-widest flex items-center gap-1.5">
              <Navigation className="w-3 h-3" /> Origin City
            </label>
            <input 
              list="city-list"
              className="input-field" 
              placeholder="e.g. Hyderabad"
              value={source}
              onChange={(e) => setSource(e.target.value)}
              required
            />
          </div>
          
          <div className="space-y-1.5">
            <label className="text-xs font-bold text-slate-500 uppercase tracking-widest flex items-center gap-1.5">
              <Navigation className="w-3 h-3 rotate-90" /> Destination
            </label>
            <input 
              list="city-list"
              className="input-field" 
              placeholder="e.g. Vijayawada"
              value={dest}
              onChange={(e) => setDest(e.target.value)}
              required
            />
          </div>

          <div className="space-y-1.5">
            <label className="text-xs font-bold text-slate-500 uppercase tracking-widest flex items-center gap-1.5">
              <Calendar className="w-3 h-3" /> Travel Date
            </label>
            <input 
              type="date"
              className="input-field"
              value={date}
              onChange={(e) => setDate(e.target.value)}
            />
          </div>

          <button type="submit" disabled={loading} className="btn-primary w-full h-[46px] flex items-center justify-center gap-2">
            {loading ? 'Searching...' : <><Search className="w-5 h-5" /> Find Routes</>}
          </button>

          <datalist id="city-list">
            {cities.map(c => <option key={c} value={c} />)}
          </datalist>
        </form>
      </div>

      {error && (
        <div className="p-4 bg-red-50 text-red-600 rounded-xl border border-red-100 font-bold text-center animate-shake">
          {error}
        </div>
      )}

      {/* Results Section */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <div className="lg:col-span-2 space-y-6">
          <div className="flex items-center gap-2 text-slate-400">
            <ListIcon className="w-5 h-5" />
            <h3 className="text-sm font-black uppercase tracking-widest">Available Schedules</h3>
          </div>
          {buses.map(bus => (
            <div key={bus.id} className="relative">
              <BusCard bus={bus} onSelect={handleBooking} />
              {bookingId === bus.id && (
                <div className="absolute inset-0 bg-white/90 backdrop-blur-sm rounded-2xl flex items-center justify-center z-10 animate-fade-in border-2 border-brand-500">
                  <div className="text-center space-y-2">
                    <CheckCircle className="w-12 h-12 text-brand-600 mx-auto animate-bounce" />
                    <p className="text-xl font-black text-slate-900">Booking Confirmed!</p>
                    <p className="text-sm font-bold text-slate-500">Redirecting to tickets...</p>
                  </div>
                </div>
              )}
            </div>
          ))}
          {!loading && buses.length === 0 && !error && (
             <div className="glass-card p-12 text-center space-y-4">
                <div className="inline-block p-4 bg-slate-100 text-slate-400 rounded-full">
                  <Search className="w-8 h-8" />
                </div>
                <p className="text-slate-500 font-medium">Enter your travel details to find available corridors.</p>
             </div>
          )}
        </div>

        <div className="space-y-6">
          <div className="flex items-center gap-2 text-slate-400">
            <MapIcon className="w-5 h-5" />
            <h3 className="text-sm font-black uppercase tracking-widest">Route Visualization</h3>
          </div>
          {source && dest ? (
            <RouteMap source={source} destination={dest} />
          ) : (
            <div className="glass-card aspect-square flex items-center justify-center text-slate-400 text-center p-8">
              <p className="text-sm font-bold uppercase tracking-wider">Map will appear once route is defined</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default FindBus;
