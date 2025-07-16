import os
from flask import Flask
from supabase import create_client, Client
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

supabase_url = os.environ.get("SUPABASE_URL")
supabase_key = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(supabase_url, supabase_key)

def create_app():
    app = Flask(__name__)
    app.secret_key = os.urandom(24)

    # Aquí registraremos los blueprints (módulos de la app)
    # from . import auth
    # app.register_blueprint(auth.bp)

    # from . import main
    # app.register_blueprint(main.bp)

    @app.route('/test')
    def test_route():
        return "<h1>La estructura del factory funciona!</h1>"

    return app
