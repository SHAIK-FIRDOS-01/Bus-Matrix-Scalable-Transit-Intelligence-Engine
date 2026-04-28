# Bus Matrix | Scalable Transit Intelligence Engine

A professional, high-performance transit management system built with Django REST Framework and React. This system implements a "Grand Corridor" model to handle complex routing, real-time geographic telemetry, and multi-passenger bookings with dynamic segment pricing.

## 🚀 Features

- **Multi-Passenger Booking**: Dynamically calculate pricing for multiple seats.
- **Segment Pricing**: Intelligent pricing based on route distances between specific nodes.
- **Enterprise Security**: JWT-based authentication with token blacklisting, rate limiting, and secure headers.
- **Modern UI**: Premium split-screen interface with glassmorphic design elements.
- **Geographic Intelligence**: Automated distance calculation using OSRM and Geopy.

## 🛠️ Technology Stack

- **Backend**: Django 6.0+, DRF, MySQL, SimpleJWT
- **Frontend**: React, Vite, Tailwind CSS v4, Lucide Icons
- **Tools**: PostCSS, Axios, Geopy

## 📦 Setup Instructions

### Backend
1. Navigate to the `backend/` directory.
2. Create a `.env` file based on `.env.example`.
3. Install dependencies: `pip install -r ../requirements.txt`.
4. Run migrations: `python manage.py migrate`.
5. Seed the fleet: `python scripts/seed_fleet.py`.
6. Start the server: `python manage.py runserver`.

### Frontend
1. Navigate to the `frontend/` directory.
2. Create a `.env` file based on `.env.example`.
3. Install dependencies: `npm install`.
4. Start development server: `npm run dev`.

## 📜 License
This project is licensed under the MIT License.
