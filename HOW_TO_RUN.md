# How to Run

## Step 1: Backend (5 minutes)

```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

✅ Backend runs on http://127.0.0.1:8000

## Step 2: Web App (3 minutes)

Open NEW terminal:

```bash
cd web
npm install
npm start
```

✅ Opens at http://localhost:3000

## Step 3: Desktop App (2 minutes)

Open NEW terminal:

```bash
cd desktop
..\backend\venv\Scripts\activate
python main.py
```

✅ Desktop window opens

## Test It!

1. Upload `backend/sample_equipment_data.csv`
2. View statistics and charts
3. Download PDF report

## Troubleshooting

**"Python not found"**
- Install from https://python.org

**"npm not found"**
- Install Node.js from https://nodejs.org

**Port already in use**
```bash
python manage.py runserver 8001
```
