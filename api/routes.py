from flask import Blueprint, render_template, abort, request, flash
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms.validators import DataRequired, Email, Length
from supabase import create_client, Client
import os
from datetime import datetime
import re
import secrets

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
