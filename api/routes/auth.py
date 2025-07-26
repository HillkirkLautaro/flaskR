from flask import Blueprint, render_template, request
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Email, Length
from supabase import create_client
from werkzeug.security import generate_password_hash
import os, re
from datetime import datetime
import requests

auth_bp = Blueprint('auth', __name__)

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

class UserCreationForm(FlaskForm):
    username = StringField('Usuario', validators=[DataRequired(), Length(min=4, max=32)])
    email = StringField('Correo electrónico', validators=[DataRequired(), Email(), Length(max=100)])
    password = PasswordField('Contraseña', validators=[DataRequired(), Length(min=8, max=128)])

def verificar_recaptcha(token):
    secret_key = os.getenv("RECAPTCHA_SECRET_KEY")
    try:
        r = requests.post(
            "https://www.google.com/recaptcha/api/siteverify",
            data={"secret": secret_key, "response": token},
            timeout=5
        )
        r.raise_for_status()
        result = r.json()
        return result.get("success", False), result
    except Exception as e:
        print(f"Error reCAPTCHA: {e}")
        return False, {"error": str(e)}

@auth_bp.route('/user_creation', methods=['GET', 'POST'])
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

                if existing.data:
                    mensaje = "El usuario o correo ya existe."
                else:
                    try:
                        hash_pw = generate_password_hash(password)
                        supabase.table('users').insert({
                            'username': username,
                            'email': email,
                            'password_hash': hash_pw,
                            'created_at': datetime.now().isoformat(),
                            'is_active': True
                        }).execute()
                        mensaje = f"¡Usuario {username} creado exitosamente!"
                    except Exception:
                        mensaje = "Hubo un error al crear el usuario."

    elif request.method == 'POST':
        mensaje = "Por favor, revisa los datos ingresados."
    
    site_key = os.getenv("RECAPTCHA_SITE_KEY")
    return render_template('user_creation.html', titulo='Registro de Usuario', mensaje=mensaje, form=form, site_key=site_key)

@auth_bp.route('/profile')
def profile():
    # user = get_current_user()
    return render_template('profile.html', titulo='Perfil de Usuario', contenido="Perfil de prueba.")
