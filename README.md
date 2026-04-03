# Chemical Equipment Parameter Visualizer

## Requirements
- Docker Desktop

## First Time Setup
```bash
git clone https://github.com/KESHVIOWHAL/Chemical-equipment-visualizer.git
cd Chemical-equipment-visualizer
docker-compose up -d
docker exec chemical-equipment-visualizer-backend-1 python manage.py migrate
```

## Run (every time after)
```bash
docker-compose up -d
```

## Access
- Frontend → http://localhost:3001
- Backend API → http://localhost:8000

## Stop
```bash
docker-compose down
```

## Usage
1. Open http://localhost:3001
2. Upload `backend/sample_equipment_data.csv` using the Upload CSV button
3. Data will appear in the dashboard
