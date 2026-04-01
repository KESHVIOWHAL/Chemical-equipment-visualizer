# Chemical Equipment Parameter Visualizer

A comprehensive multi-platform application for analyzing and visualizing chemical equipment parameters. Upload CSV data files and get instant statistical analysis, charts, and detailed reports across web, desktop, and API interfaces.

## 🚀 Features

- **CSV Data Upload & Processing** - Import equipment parameter data from CSV files
- **Statistical Analysis** - Automatic calculation of averages, totals, and distributions
- **Interactive Visualizations** - Bar charts for parameters and pie charts for equipment types
- **Multi-Platform Access** - Web app, desktop application, and REST API
- **PDF Report Generation** - Download detailed equipment analysis reports
- **Dataset History** - View and manage previously uploaded datasets
- **Real-time Data Display** - Live updates and responsive charts

## 🏗️ Architecture

This project consists of three main components:

### Backend (Django REST API)
- **Framework**: Django 5.0.2 with Django REST Framework
- **Database**: SQLite (development)
- **Features**: CSV processing, statistical calculations, PDF generation
- **Port**: http://127.0.0.1:8000

### Web Application (React)
- **Framework**: React 18.2.0
- **Charts**: Chart.js with react-chartjs-2
- **Features**: File upload, data visualization, dataset management
- **Port**: http://localhost:3000

### Desktop Application (PyQt5)
- **Framework**: PyQt5 with Matplotlib
- **Features**: Native desktop interface, offline capabilities, integrated charts
- **Platform**: Cross-platform desktop application

## 📋 Prerequisites

- **Python 3.8+** - [Download from python.org](https://python.org)
- **Node.js 16+** - [Download from nodejs.org](https://nodejs.org)
- **Git** (optional) - For cloning the repository

## 🛠️ Installation & Setup

### 1. Backend Setup (5 minutes)

```bash
cd backend
python -m venv venv
venv\Scripts\activate  # On Windows
# source venv/bin/activate  # On macOS/Linux
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

Backend runs on http://127.0.0.1:8000

### 2. Web Application Setup (3 minutes)

Open a new terminal:

```bash
cd web
npm install
npm start
```

 Web app opens at http://localhost:3000

### 3. Desktop Application Setup (2 minutes)

Open a new terminal:

```bash
cd desktop
..\backend\venv\Scripts\activate  # Use backend's virtual environment
python main.py
```

 Desktop application window opens

## 📊 Usage

### Quick Test
1. Start all three components (backend, web, desktop)
2. Upload the sample file: `backend/sample_equipment_data.csv`
3. View statistics, charts, and equipment details
4. Download PDF reports

### Data Format
Your CSV files should include these columns:
- `Equipment Name` - Unique identifier for each piece of equipment
- `Type` - Equipment category (Pump, Valve, Reactor, etc.)
- `Flowrate` - Flow rate measurement
- `Pressure` - Pressure measurement  
- `Temperature` - Temperature measurement

### API Endpoints
- `GET /api/datasets/` - List all datasets
- `POST /api/upload/` - Upload new CSV file
- `GET /api/datasets/{id}/` - Get specific dataset details
- `GET /api/datasets/{id}/pdf/` - Download PDF report

## 🔧 Troubleshooting

### Common Issues

**"Python not found"**
- Install Python from https://python.org
- Ensure Python is added to your system PATH

**"npm not found"**  
- Install Node.js from https://nodejs.org
- Restart your terminal after installation

**Port already in use**
```bash
# Change backend port
python manage.py runserver 8001

# Change web app port
PORT=3001 npm start
```

**PyQt5 installation issues**
```bash
pip install --upgrade pip
pip install PyQt5 --force-reinstall
```

**CORS errors in web app**
- Ensure backend is running on port 8000
- Check that django-cors-headers is properly configured

## 📁 Project Structure

```
├── backend/                 # Django REST API
│   ├── backend/            # Django project settings
│   ├── equipment/          # Equipment app (models, views, serializers)
│   ├── requirements.txt    # Python dependencies
│   └── sample_equipment_data.csv
├── web/                    # React web application
│   ├── src/               # React source code
│   ├── public/            # Static assets
│   └── package.json       # Node.js dependencies
├── desktop/               # PyQt5 desktop application
│   ├── main.py           # Desktop app entry point
│   └── requirements.txt  # Desktop app dependencies
└── README.md             # This file
```

## 🛡️ Dependencies

### Backend
- Django 5.0.2 - Web framework
- djangorestframework 3.14.0 - API framework
- django-cors-headers 4.3.1 - CORS handling
- pandas - Data processing
- reportlab - PDF generation
- matplotlib - Chart generation

### Web Application  
- React 18.2.0 - Frontend framework
- Chart.js 4.4.1 - Data visualization
- react-chartjs-2 5.2.0 - React Chart.js wrapper

### Desktop Application
- PyQt5 - GUI framework
- matplotlib - Chart rendering
- pandas - Data processing
- requests - API communication

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is open source and available under the [MIT License](LICENSE).

## 🆘 Support

If you encounter any issues or have questions:

1. Check the troubleshooting section above
2. Review the existing issues in the repository
3. Create a new issue with detailed information about your problem

---
