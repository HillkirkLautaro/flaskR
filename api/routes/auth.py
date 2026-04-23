from flask import Blueprint, render_template, request
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Email, Length
from supabase import create_client
from werkzeug.security import generate_password_hash
import os, re
from datetime import datetime, timezone
import requests
from google.cloud import recaptchaenterprise_v1

auth_bp = Blueprint('auth', __name__)

# Supabase config
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)


# ========================
# FORM
# ========================
class UserCreationForm(FlaskForm):
    username = StringField('Usuario', validators=[
        DataRequired(), Length(min=4, max=32)
    ])
    email = StringField('Correo electrónico', validators=[
        DataRequired(), Email(), Length(max=100)
    ])
    password = PasswordField('Contraseña', validators=[
        DataRequired(), Length(min=8, max=128)
    ])


# ========================
# RECAPTCHA
# ========================
def verificar_recaptcha_enterprise(token):
    project_id = os.getenv("GCP_PROJECT_ID")
    recaptcha_key = os.getenv("RECAPTCHA_SITE_KEY")  # misma que usás en frontend

    try:
        client = recaptchaenterprise_v1.RecaptchaEnterpriseServiceClient()

        event = recaptchaenterprise_v1.Event()
        event.site_key = recaptcha_key
        event.token = token

        assessment = recaptchaenterprise_v1.Assessment()
        assessment.event = event

        request = recaptchaenterprise_v1.CreateAssessmentRequest(
            parent=f"projects/{project_id}",
            assessment=assessment
        )

        response = client.create_assessment(request)

        # 🔴 Token inválido
        if not response.token_properties.valid:
            return False, {"error": str(response.token_properties.invalid_reason)}

        # 🔴 Acción incorrecta
        if response.token_properties.action != "submit":
            return False, {"error": "Acción inválida"}

        # ✅ Score
        score = response.risk_analysis.score

        return True, {"score": score}

    except Exception as e:
        print("ERROR reCAPTCHA Enterprise:", e)
        return False, {"error": str(e)}

# ========================
# ROUTES
# ========================
@auth_bp.route('/user_creation', methods=['GET', 'POST'])
def user_creation():
    form = UserCreationForm()
    mensaje = ""

    if form.validate_on_submit():

        # 🔹 Obtener token
        recaptcha_token = request.form.get("recaptcha_token")

        # 🔹 Debug (podés borrarlo después)
        print("TOKEN:", recaptcha_token)

        valido, resultado = verificar_recaptcha_enterprise(recaptcha_token)
        print("RECAPTCHA RESULT:", resultado)

        if not valido:
            mensaje = f"Error reCAPTCHA: {resultado}"
        else:
            username = form.username.data.strip()
            email = form.email.data.lower().strip()
            password = form.password.data

            # 🔹 Validación username
            if not re.match(r'^[a-zA-Z0-9_.-]+$', username):
                mensaje = "El usuario solo puede contener letras, números y ._-"
            else:
                try:
                    # 🔹 Verificar email
                    existing_email = supabase.table('users') \
                        .select('id') \
                        .eq('email', email) \
                        .execute()

                    # 🔹 Verificar username
                    existing_username = supabase.table('users') \
                        .select('id') \
                        .eq('username', username) \
                        .execute()

                    if existing_email.data or existing_username.data:
                        mensaje = "El usuario o correo ya existe."
                    else:
                        # 🔹 Hash password
                        hash_pw = generate_password_hash(password)

                        # 🔹 Insert user
                        supabase.table('users').insert({
                            'username': username,
                            'email': email,
                            'password_hash': hash_pw,
                            'created_at': datetime.now(timezone.utc).isoformat(),
                            'is_active': True
                        }).execute()

                        mensaje = f"¡Usuario {username} creado exitosamente!"

                except Exception as e:
                    print("ERROR DB:", e)
                    mensaje = "Hubo un error al crear el usuario."

    elif request.method == 'POST':
        print("FORM ERRORS:", form.errors)
        mensaje = "Por favor, revisa los datos ingresados."

    site_key = os.getenv("RECAPTCHA_SITE_KEY")

    return render_template(
        'user_creation.html',
        titulo='Registro de Usuario',
        mensaje=mensaje,
        form=form,
        site_key=site_key
    )



@auth_bp.route('/profile')
def profile():
    return render_template(
        'profile.html',
        titulo='Perfil de Usuario',
        contenido="Perfil de prueba."
    )