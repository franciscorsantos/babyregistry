import os
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'bebe-registry-super-secret-key-2026')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', f'sqlite:///{os.path.join(BASE_DIR, "bebe_registry.db")}')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Mercado Pago SDK Configuration
    MERCADO_PAGO_ACCESS_TOKEN = os.environ.get('MERCADO_PAGO_ACCESS_TOKEN', '')
    WEBHOOK_URL = os.environ.get('WEBHOOK_URL', 'http://localhost:5000/webhook')
