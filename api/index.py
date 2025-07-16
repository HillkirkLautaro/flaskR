import sys
import os

sys.path.insert(0, os.path.dirname(__file__))  # agrega carpeta actual a sys.path

from app import app

# This is required for Vercel to recognize the WSGI application
handler = app.wsgi_app
