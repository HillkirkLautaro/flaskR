import os
from flask import Flask, render_template, request, redirect, url_for, flash, session
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.urandom(24) # Necesario para los mensajes flash

# Configuración de Supabase
supabase_url = os.environ.get("SUPABASE_URL")
supabase_key = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(supabase_url, supabase_key)

@app.route('/')
def index():
    # Lógica para mostrar el feed de publicaciones (se implementará más adelante)
    return "<h1>Bienvenido al Microblog</h1><p>La configuración funciona correctamente.</p>"

if __name__ == '__main__':
    app.run(debug=True)
