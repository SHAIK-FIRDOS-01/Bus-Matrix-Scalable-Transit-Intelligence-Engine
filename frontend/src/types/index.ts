export interface Bus {
  id: number;
  bus_name: string;
  source: string;
  dest: string;
  nos: number;
  rem: number;
  price: string;
  date: string;
  time: string;
  distance_km: number;
  travel_time_hrs: number;
  source_lat: number;
  source_lon: number;
  dest_lat: number;
  dest_lon: number;
  route_nodes: string;
  arrival_time_str: string;
  dynamic_price?: number;
  target_date?: string;
  display_source?: string;
  display_dest?: string;
}

export interface Booking {
  id: number;
  bus_name: string;
  source: string;
  dest: string;
  nos: number;
  price: string;
  date: string;
  time: string;
  status: 'B' | 'C';
  user: number;
  bus: number;
}

export interface User {
  id: number;
  username: string;
  email: string;
}

export interface AuthResponse {
  user: User;
  access: string;
  refresh: string;
}
