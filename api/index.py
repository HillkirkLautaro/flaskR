
from app import app

# This is required for Vercel to recognize the WSGI application
handler = app.wsgi_app
