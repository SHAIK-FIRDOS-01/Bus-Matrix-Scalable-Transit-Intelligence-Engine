import React, { useEffect, useState } from 'react';
import api from '../services/api';
import type { Booking } from '../types';

import { Ticket, Calendar, Clock, MapPin, XCircle, RefreshCw } from 'lucide-react';

const Bookings: React.FC = () => {
  const [bookings, setBookings] = useState<Booking[]>([]);
  const [loading, setLoading] = useState(true);

  const fetchBookings = async () => {
    setLoading(true);
    try {
      const res = await api.get('bookings/');
      setBookings(res.data);
    } catch (err) {
      console.error('Error fetching bookings:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchBookings();
  }, []);

  const handleCancel = async (id: number) => {
    if (window.confirm('Are you sure you want to cancel this booking?')) {
      try {
        await api.post(`bookings/${id}/cancel/`);
        fetchBookings();
      } catch (err) {
        alert('Failed to cancel booking');
      }
    }
  };

  if (loading) return <div className="pt-24 text-center font-bold text-slate-400">Loading your tickets...</div>;

  return (
    <div className="pt-24 pb-12 px-4 max-w-7xl mx-auto space-y-8">
      <div className="flex justify-between items-center">
        <h2 className="text-3xl font-black text-slate-900 tracking-tight">My Bookings</h2>
        <button onClick={fetchBookings} className="p-2 text-brand-600 hover:bg-brand-50 rounded-lg transition-colors">
          <RefreshCw className="w-5 h-5" />
        </button>
      </div>

      {bookings.length === 0 ? (
        <div className="glass-card p-16 text-center space-y-4">
          <div className="inline-block p-6 bg-slate-100 text-slate-400 rounded-full">
            <Ticket className="w-12 h-12" />
          </div>
          <p className="text-slate-500 font-bold text-xl">No active bookings found.</p>
          <p className="text-slate-400">Your future travel plans will appear here.</p>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {bookings.map(book => (
            <div key={book.id} className="glass-card p-6 space-y-6 relative overflow-hidden group">
               <div className="absolute top-0 right-0 p-3">
                  <span className={`text-[10px] font-black uppercase tracking-widest px-2 py-1 rounded ${book.status === 'B' ? 'bg-green-100 text-green-700' : 'bg-red-100 text-red-700'}`}>
                    {book.status === 'B' ? 'Confirmed' : 'Cancelled'}
                  </span>
               </div>

               <div className="space-y-1">
                  <h3 className="text-xl font-black text-slate-900">{book.bus_name}</h3>
                  <div className="flex items-center gap-4 text-xs font-bold text-slate-400 uppercase tracking-widest">
                    <span className="flex items-center gap-1"><Calendar className="w-3 h-3" /> {book.date}</span>
                    <span className="flex items-center gap-1"><Clock className="w-3 h-3" /> {book.time}</span>
                  </div>
               </div>

               <div className="flex items-center gap-4 text-sm font-bold text-slate-600">
                  <div className="flex-1 flex items-center gap-2 truncate">
                    <MapPin className="w-4 h-4 text-brand-500" />
                    <span>{book.source}</span>
                  </div>
                  <div className="flex-1 flex items-center gap-2 truncate">
                    <MapPin className="w-4 h-4 text-brand-500" />
                    <span>{book.dest}</span>
                  </div>
               </div>

               <div className="pt-4 border-t border-slate-100 flex justify-between items-center">
                  <div>
                    <p className="text-[10px] font-bold text-slate-400 uppercase tracking-widest">Tickets / Price</p>
                    <p className="text-lg font-black text-slate-900">{book.nos} Pax / ₹{book.price}</p>
                  </div>
                  {book.status === 'B' && (
                    <button 
                      onClick={() => handleCancel(book.id)}
                      className="p-2 text-slate-400 hover:text-red-600 hover:bg-red-50 rounded-lg transition-all"
                      title="Cancel Ticket"
                    >
                      <XCircle className="w-6 h-6" />
                    </button>
                  )}
               </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default Bookings;
