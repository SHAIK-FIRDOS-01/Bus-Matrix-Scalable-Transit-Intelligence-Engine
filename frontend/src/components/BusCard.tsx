import React, { useState } from 'react';
import type { Bus as BusType } from '../types';

import { Clock, MapPin, Users, IndianRupee, ArrowRight, Minus, Plus } from 'lucide-react';

interface BusCardProps {
  bus: BusType;
  onSelect: (bus: BusType, seats: number) => void;
}

const BusCard: React.FC<BusCardProps> = ({ bus, onSelect }) => {
  const [seats, setSeats] = useState(1);
  const basePrice = parseFloat(bus.dynamic_price?.toString() || bus.price.toString());
  const totalPrice = (basePrice * seats).toFixed(2);

  const increment = () => {
    if (seats < bus.rem) setSeats(s => s + 1);
  };

  const decrement = () => {
    if (seats > 1) setSeats(s => s - 1);
  };

  return (
    <div className="glass-card p-6 flex flex-col md:flex-row justify-between items-start md:items-center gap-6 group hover:-translate-y-1 transition-all duration-300">
      <div className="flex-1 space-y-4">
        <div className="flex items-center gap-3">
          <div className="p-3 bg-brand-50 text-brand-600 rounded-2xl group-hover:bg-brand-600 group-hover:text-white transition-colors duration-300">
            <Clock className="w-6 h-6" />
          </div>
          <div>
            <h3 className="text-xl font-extrabold text-slate-900 leading-tight">{bus.bus_name}</h3>
            <p className="text-sm font-medium text-slate-500 uppercase tracking-wider">{bus.time} Departure</p>
          </div>
        </div>
        
        <div className="flex items-center gap-4 text-slate-600">
          <div className="flex items-center gap-1.5 bg-slate-100 px-3 py-1 rounded-lg">
            <MapPin className="w-4 h-4 text-brand-500" />
            <span className="text-sm font-bold">{bus.display_source || bus.source}</span>
          </div>
          <ArrowRight className="w-4 h-4 text-slate-400" />
          <div className="flex items-center gap-1.5 bg-slate-100 px-3 py-1 rounded-lg">
            <MapPin className="w-4 h-4 text-brand-500" />
            <span className="text-sm font-bold">{bus.display_dest || bus.dest}</span>
          </div>
        </div>
      </div>

      <div className="flex flex-col items-center md:items-end gap-4 w-full md:w-auto border-t md:border-t-0 md:border-l border-slate-100 pt-4 md:pt-0 md:pl-8">
        <div className="flex items-center justify-between w-full md:justify-end gap-8">
          {/* Seat Selector */}
          <div className="space-y-1.5">
            <p className="text-[10px] font-bold text-slate-400 uppercase tracking-widest text-center md:text-right">Select Passengers</p>
            <div className="flex items-center gap-3 bg-slate-100 p-1 rounded-xl">
              <button 
                onClick={decrement}
                disabled={seats <= 1}
                className="p-1.5 bg-white rounded-lg shadow-sm disabled:opacity-30 hover:text-brand-600 transition-colors"
              >
                <Minus className="w-4 h-4" />
              </button>
              <span className="w-6 text-center font-black text-slate-700">{seats}</span>
              <button 
                onClick={increment}
                disabled={seats >= bus.rem}
                className="p-1.5 bg-white rounded-lg shadow-sm disabled:opacity-30 hover:text-brand-600 transition-colors"
              >
                <Plus className="w-4 h-4" />
              </button>
            </div>
          </div>

          <div className="text-right">
            <p className="text-[10px] font-bold text-slate-400 uppercase tracking-widest">Total Price</p>
            <div className="flex items-center justify-end gap-1 text-2xl font-black text-brand-600">
              <IndianRupee className="w-5 h-5" />
              <span>{totalPrice}</span>
            </div>
            <div className="flex items-center justify-end gap-1.5 text-xs font-bold text-slate-400 uppercase tracking-widest mt-1">
              <Users className="w-3.5 h-3.5" />
              <span>{bus.rem} Seats Left</span>
            </div>
          </div>
        </div>

        <button 
          onClick={() => onSelect(bus, seats)}
          className="btn-primary w-full md:w-auto py-3 px-8 flex items-center justify-center gap-2"
        >
          Book {seats} {seats === 1 ? 'Seat' : 'Seats'}
        </button>
      </div>
    </div>
  );
};

export default BusCard;
