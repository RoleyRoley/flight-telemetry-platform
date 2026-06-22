# Flight Telemetry Platform

A comprehensive real-time flight telemetry monitoring and anomaly detection system built with FastAPI and PostgreSQL. This platform captures, processes, and analyzes aircraft sensor data to generate intelligent alerts for operational anomalies.

## 🎯 Overview

The Flight Telemetry Platform provides a production-ready API for managing flight data, detecting anomalies in real-time, and maintaining alert systems for aviation operations. It includes a simulator for testing and development purposes.

### Key Use Cases
- **Real-time Monitoring**: Ingest telemetry data from aircraft sensors continuously
- **Anomaly Detection**: Automatically detect and alert on critical aircraft anomalies
- **Flight Tracking**: Manage flight schedules, aircraft assignments, and routes
- **Alert Management**: Query and manage system-generated alerts for operational oversight
- **Testing & Simulation**: Simulate realistic flight scenarios for development and testing

## ✨ Features

- **RESTful API** - Fully-featured FastAPI backend with automatic documentation
- **Real-time Telemetry Processing** - Handle continuous sensor data streams
- **Anomaly Detection** - Intelligent detection of engine overheating, fuel leaks, and rapid altitude loss
- **Alert Generation** - Automatic alert creation with severity levels
- **Flight Management** - Track flights, aircraft, and operational metadata
- **Database Persistence** - PostgreSQL with SQLAlchemy ORM
- **Health Checks** - Built-in API health and database connectivity monitoring
- **Flight Simulator** - Python simulator for testing telemetry ingestion pipelines

## 🏗️ Architecture

```
flight-telemetry-platform/
├── backend/                          # FastAPI application
│   ├── app/
│   │   ├── main.py                  # FastAPI app initialization
│   │   ├── database.py              # SQLAlchemy setup & session management
│   │   ├── models.py                # SQLAlchemy ORM models (Aircraft, Flight, Telemetry, Alert)
│   │   ├── schemas.py               # Pydantic request/response schemas
│   │   ├── routes/
│   │   │   ├── telemetry.py         # POST/GET telemetry data endpoints
│   │   │   ├── flights.py           # Flight management endpoints
│   │   │   └── alerts.py            # Alert query and retrieval endpoints
│   │   └── services/
│   │       └── anomaly_detector.py  # Anomaly detection logic
│   ├── requirements.txt             # Python dependencies
│   ├── .env                         # Environment configuration (database URL)
│   └── seed.py                      # Database seeding script
│
└── simulator/                       # Flight telemetry simulator
    └── simulator.py                 # Synthetic telemetry data generator
```

## 📋 Prerequisites

- **Python 3.8+**
- **PostgreSQL 12+**
- **pip** or virtual environment manager
- Git for version control

## 🚀 Installation

### 1. Clone the Repository

```bash
git clone <repository-url>
cd flight-telemetry-platform
```

### 2. Set Up Python Virtual Environment

```bash
# Create virtual environment
python -m venv .venv

# Activate it
# On Windows:
.venv\Scripts\activate
# On macOS/Linux:
source .venv/bin/activate
```

### 3. Install Backend Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the `backend/` directory:

```bash
DATABASE_URL=postgresql+psycopg2://postgres:password@localhost:5432/flight_telemetry
```

**Configuration Variables:**
- `DATABASE_URL`: PostgreSQL connection string
  - Format: `postgresql+psycopg2://username:password@host:port/database`
  - Ensure PostgreSQL is running and the database exists

### 5. Initialize Database

The database tables are created automatically when the application starts. Optionally, seed with sample data:

```bash
cd backend
python seed.py
```

## 🏃 Quick Start

### Start the Backend API

```bash
cd backend
uvicorn app.main:app --reload
```

The API will be available at `http://127.0.0.1:8000`

**Key Endpoints:**
- `GET /` - Root endpoint with navigation
- `GET /health` - Health check
- `GET /db-test` - Database connectivity test
- `GET /docs` - Interactive API documentation (Swagger UI)

### Run the Simulator

In another terminal:

```bash
cd simulator
python simulator.py
```

The simulator will generate telemetry data and send it to the API at 1-second intervals.

## 📡 API Documentation

### Interactive API Docs

Once the backend is running, visit:
- **Swagger UI**: `http://127.0.0.1:8000/docs`
- **ReDoc**: `http://127.0.0.1:8000/redoc`

### Key Endpoints

#### Telemetry
- `POST /telemetry/` - Submit aircraft telemetry data
- `GET /telemetry/` - Query telemetry records

**Sample Telemetry Data:**
```json
{
  "flight_id": 1,
  "altitude_ft": 35000,
  "ground_speed_kts": 450,
  "fuel_percentage": 65.5,
  "engine_temp_c": 85.2,
  "flight_phase": "cruise"
}
```

#### Flights
- `GET /flights/{flight_id}` - Get flight details by ID
- `GET /flights/` - List all flights

#### Alerts
- `GET /alerts/{flight_id}` - Get alerts for a specific flight
- `GET /alerts/` - Query all alerts

## ⚙️ Configuration

### Database Setup

1. **Create PostgreSQL Database:**
   ```bash
   createdb flight_telemetry
   ```

2. **Update `.env`** with your connection details

3. **Verify Connection:**
   ```bash
   curl http://127.0.0.1:8000/db-test
   ```

### Simulator Configuration

Edit `simulator/simulator.py` to adjust:
- `FLIGHT_ID` - Which flight to simulate
- `FAULT_CHANCE` - Probability of triggering anomalies (0-1)
- `FORCED_FAULT` - Force a specific anomaly type for testing

## 🔍 Anomaly Detection

The system detects three primary anomaly types:

1. **Engine Overheat** - Engine temperature exceeds safe threshold
2. **Fuel Leak** - Fuel percentage drops unexpectedly
3. **Rapid Altitude Loss** - Sudden altitude decrease below normal descent rate

Detected anomalies automatically generate alerts stored in the database.

## 👨‍💻 Development

### Adding a New Feature

1. Create a feature branch:
   ```bash
   git checkout main
   git pull origin main
   git checkout -b feature/your-feature-name
   ```

2. Make your changes and test locally

3. Commit with clear messages:
   ```bash
   git add .
   git commit -m "Add: descriptive message of changes"
   ```

4. Push to remote:
   ```bash
   git push -u origin feature/your-feature-name
   ```

5. Open a Pull Request on GitHub with description and testing notes

### Running Tests

```bash
# Add pytest to requirements.txt and create tests/ directory
pytest tests/ -v
```

### Code Style

This project follows PEP 8 conventions. Consider using:
- `black` for code formatting
- `flake8` for linting
- `mypy` for type checking

## 🐛 Troubleshooting

### Database Connection Error

**Error:** `DATABASE_URL environment variable is not set`

**Solution:**
- Verify `.env` file exists in `backend/` directory
- Check `DATABASE_URL` is set correctly
- Ensure PostgreSQL is running and database exists

### API Port Already in Use

**Error:** `Address already in use [('127.0.0.1', 8000)]`

**Solution:**
```bash
# Change port in startup command
uvicorn app.main:app --reload --port 8001
```

### Simulator Connection Refused

**Error:** `Connection error: [Errno 111] Connection refused`

**Solution:**
- Ensure backend API is running on `http://127.0.0.1:8000`
- Check firewall/network settings
- Verify `API_URL` in `simulator.py`

### Import Errors

**Solution:**
- Activate virtual environment
- Reinstall dependencies: `pip install -r requirements.txt`
- Verify you're in the correct directory when running commands

## 📦 Dependencies

### Core
- **FastAPI** - Web framework for building APIs
- **SQLAlchemy** - ORM for database operations
- **Pydantic** - Data validation
- **psycopg2-binary** - PostgreSQL adapter
- **python-dotenv** - Environment variable management
- **Uvicorn** - ASGI server

See [backend/requirements.txt](backend/requirements.txt) for complete dependency list and versions.

## 📄 Database Schema

### Key Tables

**Aircraft**
- `id` - Primary key
- `aircraft_code` - Unique identifier (e.g., "A320")
- `model` - Descriptive model name
- `flights` - Relationship to Flight records

**Flight**
- `id` - Primary key
- `flight_number` - Unique flight identifier
- `aircraft_id` - Foreign key to Aircraft
- `departure_airport` - IATA code
- `arrival_airport` - IATA code
- `scheduled_departure` - ISO 8601 timestamp
- `actual_departure` - ISO 8601 timestamp
- `estimated_arrival` - ISO 8601 timestamp
- `actual_arrival` - ISO 8601 timestamp
- `status` - Flight status (scheduled, in_flight, landed)

**Telemetry**
- `id` - Primary key
- `flight_id` - Foreign key to Flight
- `altitude_ft` - Altitude in feet
- `ground_speed_kts` - Speed in knots
- `fuel_percentage` - Remaining fuel (0-100)
- `engine_temp_c` - Engine temperature in Celsius
- `flight_phase` - Current phase (preflight, takeoff, climb, cruise, descent, landing)
- `timestamp` - Data collection timestamp

**Alert**
- `id` - Primary key
- `flight_id` - Foreign key to Flight
- `alert_type` - Type of anomaly detected
- `severity` - Alert severity level
- `message` - Human-readable alert description
- `timestamp` - When alert was generated

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/AmazingFeature`
3. Commit changes: `git commit -m 'Add AmazingFeature'`
4. Push to branch: `git push origin feature/AmazingFeature`
5. Open a Pull Request

### Pull Request Guidelines
- Provide clear description of changes
- Include any testing performed
- Reference related issues if applicable
- Ensure no sensitive data (passwords, API keys) is committed

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## ✉️ Support

For issues, questions, or contributions:
1. Check existing GitHub issues
2. Create a new issue with detailed description
3. Include relevant logs and error messages
4. Specify your environment (OS, Python version, etc.)

## 🗓️ Version History

**v1.0.0** - Initial release
- Core API endpoints for telemetry, flights, and alerts
- Anomaly detection engine
- Flight simulator for testing
- PostgreSQL database persistence

---

**Built with ❤️ for aviation operations**
