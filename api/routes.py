from flask import Blueprint, render_template, abort, request
from supabase import create_client, Client
import os
from datetime import datetime

# Crear el blueprint con el prefijo de ruta
main_bp = Blueprint('main', __name__)

SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

@main_bp.route('/')
def index():
    return render_template('index.html', nombre='Usuario')

@main_bp.route('/about')
def about():
    return render_template('about.html', titulo='Acerca de', contenido="Esta es una demo con Flask y Supabase en Vercel.")


@main_bp.route('/encuesta', methods=['GET', 'POST'])
def encuesta():
    mensaje = ""
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        email = request.form.get('email')
        opinion = request.form.get('opinion')
        fecha = datetime.now().isoformat()
        data = supabase.table('encuestas').insert({
            'name': nombre,
            'email': email,
            'opinion': opinion,
            'date_time': fecha
        }).execute()
        mensaje = "¡Gracias por tu opinión, {}!".format(nombre)
    return render_template('encuesta.html', titulo='Encuesta', contenido=mensaje)
