# Chemical Equipment Parameter Visualizer

A hybrid web and desktop application for visualizing and analyzing chemical equipment data.

##  Quick Start

### 1. Backend Setup
```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

### 2. Web Frontend
```bash
cd web
npm install
npm start
```

### 3. Desktop App
```bash
cd desktop
..\backend\venv\Scripts\activate
python main.py
```

## 📊 Features

-  CSV file upload (Web & Desktop)
- Data analysis with Pandas
- Interactive charts (Chart.js & Matplotlib)
-  Dataset history (last 5 uploads)
-  PDF report generation
-  RESTful API backend
-  SQLite database

## 🛠️ Tech Stack

- **Backend:** Django + Django REST Framework
- **Web:** React.js + Chart.js
- **Desktop:** PyQt5 + Matplotlib
- **Database:** SQLite
- **Data Processing:** Pandas

## 📝 CSV Format

```csv
Equipment Name,Type,Flowrate,Pressure,Temperature
Pump A,Pump,120,30,80
Valve B,Valve,60,20,50
```

## 📖 Documentation

- `HOW_TO_RUN.md` - Simple running instructions
- `SETUP_GUIDE.md` - Detailed setup guide
- Sample data: `backend/sample_equipment_data.csv`

## 🎯 API Endpoints

- `POST /api/upload/` - Upload CSV
- `GET /api/datasets/` - List datasets
- `GET /api/datasets/{id}/` - Get dataset detail
- `GET /api/datasets/{id}/pdf/` - Download PDF

## 📞 Support

For issues, check the documentation files or create a GitHub issue.
