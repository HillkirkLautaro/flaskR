from dotenv import load_dotenv
import requests
import os
# Cargar las variables de entorno desde el archivo .env
load_dotenv()

from flask import Blueprint, render_template, abort, request, flash
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, PasswordField
from wtforms.validators import DataRequired, Email, Length
from supabase import create_client, Client
import os
from datetime import datetime
import re
import secrets
from werkzeug.security import generate_password_hash
from datetime import datetime, timedelta
from flask import request

# Crear el blueprint con el prefijo de ruta
main_bp = Blueprint('main', __name__)


SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Flask-WTF CSRF protection
class EncuestaForm(FlaskForm):
    nombre = StringField('Nombre', validators=[DataRequired(), Length(max=100)])
    email = StringField('Correo electrónico', validators=[DataRequired(), Email(), Length(max=100)])
    opinion = TextAreaField('Opinión', validators=[DataRequired(), Length(max=1000)])

class UserCreationForm(FlaskForm):
    username = StringField('Usuario', validators=[DataRequired(), Length(min=4, max=32)])
    email = StringField('Correo electrónico', validators=[DataRequired(), Email(), Length(max=100)])
    password = PasswordField('Contraseña', validators=[DataRequired(), Length(min=8, max=128)])

def verificar_recaptcha(token):
    secret_key = os.getenv("RECAPTCHA_SECRET_KEY")
    respuesta = requests.post(
        "https://www.google.com/recaptcha/api/siteverify",
        data={
            "secret": secret_key,
            "response": token
        }
    )
    resultado = respuesta.json()
    return resultado.get("success", False), resultado

def is_valid_email(email):
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)

@main_bp.route('/')
def index():
    return render_template('index.html', nombre='Usuario')

@main_bp.route('/about')
def about():
    return render_template('about.html', titulo='Acerca de', contenido="Esta es una demo con Flask y Supabase en Vercel.")


@main_bp.route('/encuesta', methods=['GET', 'POST'])
def encuesta():
    form = EncuestaForm()
    mensaje = ""

    if form.validate_on_submit():
        ip_address = request.headers.get('X-Forwarded-For', request.remote_addr)
        if ip_address:
            ip_address = ip_address.split(',')[0].strip()
        else:
            ip_address = '0.0.0.0'  # fallback

        # Obtener la fecha y hora actual
        from datetime import datetime, timedelta    
        ahora = datetime.now()
        hace_una_hora = ahora - timedelta(hours=1)

        # Buscar envíos recientes de esta IP en la última hora
        try:
            respuesta = supabase.table('encuestas').select('date_time').eq('ip_address', ip_address).execute()
            envios_recientes = [
                r['date_time'] for r in respuesta.data
                if datetime.fromisoformat(r['date_time']) > hace_una_hora
            ]
        except Exception as e:
            envios_recientes = []
            print("Error al consultar Supabase:", e)

        if len(envios_recientes) >= 2:
            mensaje = "Has alcanzado el límite de envíos desde tu IP. Por favor, intentá más tarde."
        else:
            nombre = form.nombre.data
            email = form.email.data
            opinion = form.opinion.data
            fecha = ahora.isoformat()

            try:
                supabase.table('encuestas').insert({
                    'name': nombre,
                    'email': email,
                    'opinion': opinion,
                    'date_time': fecha,
                    'ip_address': ip_address
                }).execute()
                mensaje = f"¡Gracias por tu opinión, {nombre}!"
            except Exception as e:
                print("Error al insertar encuesta:", e)
                mensaje = "Hubo un error al guardar tu opinión. Intenta nuevamente."

    elif request.method == 'POST':
        mensaje = "Por favor, revisa los datos ingresados."

    return render_template('encuesta.html', titulo='Encuesta', contenido=mensaje, form=form)
@main_bp.route('/user_creation', methods=['GET', 'POST'])
def user_creation():
    form = UserCreationForm()
    mensaje = ""
    if form.validate_on_submit():
        recaptcha_token = request.form.get("recaptcha_token")
        valido, resultado = verificar_recaptcha(recaptcha_token)

        if not valido:
            mensaje = "Fallo la verificación reCAPTCHA. ¿Sos un bot?"
        else:
            username = form.username.data.strip()
            email = form.email.data.lower().strip()
            password = form.password.data

            if not re.match(r'^[a-zA-Z0-9_.-]+$', username):
                mensaje = "El usuario solo puede contener letras, números y ._-"
            else:
                existing = supabase.table('users').select('*').or_(
                    f"email.eq.{email},username.eq.{username}"
                ).execute()

                if existing.data and len(existing.data) > 0:
                    mensaje = "El usuario o correo ya existe."
                else:
                    try:
                        password_hash = generate_password_hash(password)
                        supabase.table('users').insert({
                            'username': username,
                            'email': email,
                            'password_hash': password_hash,
                            'created_at': datetime.now().isoformat(),
                            'is_active': True
                        }).execute()
                        mensaje = f"¡Usuario {username} creado exitosamente!"
                    except Exception:
                        mensaje = "Hubo un error al crear el usuario. Intenta nuevamente."
    elif request.method == 'POST':
        mensaje = "Por favor, revisa los datos ingresados."
    
    site_key = os.getenv("RECAPTCHA_SITE_KEY")  # Pasar al HTML
    return render_template('user_creation.html', titulo='Registro de Usuario', mensaje=mensaje, form=form, site_key=site_key)