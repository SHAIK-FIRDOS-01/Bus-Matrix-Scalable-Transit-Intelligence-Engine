import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import api from '../services/api';
import { Bus, Lock, User as UserIcon } from 'lucide-react';

const Login: React.FC = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const { login } = useAuth();
  const navigate = useNavigate();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    try {
      const res = await api.post('auth/login/', { username, password });
      login(res.data.access, res.data.refresh, res.data.user);
      navigate('/');
    } catch (err: any) {
      setError(err.response?.data?.error || 'Invalid credentials');
    }
  };

  return (
    <div className="min-h-screen flex flex-col md:flex-row bg-white">
      {/* Left Side: Visual/Branding */}
      <div className="hidden md:flex md:w-1/2 lg:w-3/5 bg-brand-900 relative overflow-hidden">
        <img 
          src="/login-bg.png" 
          alt="Bus Background" 
          className="absolute inset-0 w-full h-full object-cover opacity-60 mix-blend-overlay"
        />
        <div className="absolute inset-0 bg-gradient-to-t from-brand-950 via-transparent to-transparent opacity-80" />
        
        <div className="relative z-10 p-16 flex flex-col justify-end h-full text-white max-w-2xl">
          <div className="mb-8 inline-flex items-center gap-3 px-4 py-2 bg-white/10 backdrop-blur-md rounded-full border border-white/20 w-fit animate-fade-in">
            <Bus className="w-5 h-5" />
            <span className="text-sm font-bold tracking-widest uppercase">Premium Transit Experience</span>
          </div>
          <h1 className="text-5xl lg:text-7xl font-black tracking-tighter leading-tight mb-6 animate-slide-up">
            Your Journey <br />
            <span className="text-brand-400">Begins Here.</span>
          </h1>
          <p className="text-xl text-slate-300 font-medium leading-relaxed max-w-lg animate-slide-up" style={{ animationDelay: '100ms' }}>
            Manage your bus corridors, track real-time bookings, and optimize your fleet with ABC Transit's next-gen matrix platform.
          </p>
        </div>
        
        {/* Decorative elements */}
        <div className="absolute top-[-10%] right-[-10%] w-64 h-64 bg-brand-500 rounded-full blur-[120px] opacity-20" />
        <div className="absolute bottom-[20%] left-[-5%] w-48 h-48 bg-brand-400 rounded-full blur-[100px] opacity-20" />
      </div>

      {/* Right Side: Login Form */}
      <div className="flex-1 flex items-center justify-center p-8 lg:p-16 bg-slate-50/50">
        <div className="w-full max-w-[440px] space-y-10 animate-fade-in" style={{ animationDelay: '200ms' }}>
          <div className="space-y-3">
            <div className="md:hidden inline-block p-3 bg-brand-600 text-white rounded-2xl shadow-xl shadow-brand-200 mb-4">
              <Bus className="w-6 h-6" />
            </div>
            <h2 className="text-4xl font-black tracking-tight text-slate-900">Welcome Back</h2>
            <p className="text-slate-500 font-semibold">Enter your credentials to access your dashboard</p>
          </div>

          <form onSubmit={handleSubmit} className="space-y-6">
            <div className="space-y-2">
              <label className="text-xs font-bold text-slate-400 uppercase tracking-widest flex items-center gap-2 px-1">
                <UserIcon className="w-3.5 h-3.5" /> Username
              </label>
              <input 
                className="input-field py-3.5" 
                placeholder="firdos_sk"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                required 
              />
            </div>

            <div className="space-y-2">
              <div className="flex justify-between items-end px-1">
                <label className="text-xs font-bold text-slate-400 uppercase tracking-widest flex items-center gap-2">
                  <Lock className="w-3.5 h-3.5" /> Password
                </label>
                <a href="#" className="text-xs font-bold text-brand-600 hover:text-brand-700 transition-colors">Forgot?</a>
              </div>
              <input 
                type="password"
                className="input-field py-3.5" 
                placeholder="••••••••"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required 
              />
            </div>

            {error && (
              <div className="p-3 bg-red-50 border border-red-100 rounded-xl flex items-center gap-2 text-red-600 text-sm font-bold animate-shake">
                <span>⚠️ {error}</span>
              </div>
            )}

            <button type="submit" className="btn-primary w-full py-4 text-lg mt-4 shadow-xl shadow-brand-600/20">
              Sign In to Matrix
            </button>
          </form>

          <div className="pt-6 border-t border-slate-200">
            <p className="text-center text-slate-500 font-semibold">
              Don't have an account? <Link to="/register" className="text-brand-600 font-bold hover:text-brand-700 transition-colors">Join ABC Transit</Link>
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Login;
