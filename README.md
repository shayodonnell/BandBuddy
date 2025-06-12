# BandBuddy

BandBuddy is a simple Flask web application for musicians to connect and share updates. It uses Flask, SQLAlchemy and Flask-Migrate for the backend and Bootstrap for the UI.

## Environment Setup

1. Create a Python virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Initialize the database:
   ```bash
   python db_create.py
   ```

## Environment Variables

The application can be configured using the following environment variables:

- `SECRET_KEY` – Flask secret key. Defaults to `huak-tuah`.
- `SQLALCHEMY_DATABASE_URI` – Database connection URI. Defaults to a local
  SQLite database at `app.db`.
- `SQLALCHEMY_TRACK_MODIFICATIONS` – Set to `True` to enable SQLAlchemy event
  notifications. Defaults to `False`.

## Running the App

Start the development server with:
```bash
python run.py
```
The application will be available at `http://localhost:5000/`.

