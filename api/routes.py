from dotenv import load_dotenv
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
        nombre = form.nombre.data
        email = form.email.data
        opinion = form.opinion.data
        fecha = datetime.now().isoformat()
        try:
            supabase.table('encuestas').insert({
                'name': nombre,
                'email': email,
                'opinion': opinion,
                'date_time': fecha
            }).execute()
            mensaje = f"¡Gracias por tu opinión, {nombre}!"
        except Exception:
            mensaje = "Hubo un error al guardar tu opinión. Intenta nuevamente."
    elif request.method == 'POST':
        mensaje = "Por favor, revisa los datos ingresados."
    return render_template('encuesta.html', titulo='Encuesta', contenido=mensaje, form=form)

@main_bp.route('/user_creation', methods=['GET', 'POST'])
def user_creation():
    form = UserCreationForm()
    mensaje = ""
    if form.validate_on_submit():
        username = form.username.data.strip()
        email = form.email.data.lower().strip()
        password = form.password.data

        # Validación extra: solo caracteres permitidos en username
        if not re.match(r'^[a-zA-Z0-9_.-]+$', username):
            mensaje = "El usuario solo puede contener letras, números y ._-"
        else:
            # Verificar si el usuario o email ya existen
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
    return render_template('user_creation.html', titulo='Registro de Usuario', mensaje=mensaje, form=form)
