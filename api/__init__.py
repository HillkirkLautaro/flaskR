from flask import Flask
from flask_wtf.csrf import CSRFProtect
from api.routes import all_blueprints

from dotenv import load_dotenv
import os
from supabase import create_client

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError("Faltan variables de entorno SUPABASE_URL o SUPABASE_KEY")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def create_app():
    app = Flask(__name__)
    app.secret_key = os.getenv("SECRET_KEY", "dev_key")

    CSRFProtect(app)

    for bp in all_blueprints:
        app.register_blueprint(bp)

    # Podés pasar supabase como global o adjuntarlo al app
    app.supabase = supabase

    return app
