from flask import Blueprint, render_template, request
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms.validators import DataRequired, Email, Length
from supabase import create_client
from datetime import datetime, timedelta
import os
from api.utils.supabase import supabase # Importa el cliente Supabase desde utils


encuesta_bp = Blueprint('encuesta', __name__)

# Formulario
class EncuestaForm(FlaskForm):
    nombre = StringField('Nombre', validators=[DataRequired(), Length(max=100)])
    email = StringField('Correo electrónico', validators=[DataRequired(), Email(), Length(max=100)])
    opinion = TextAreaField('Opinión', validators=[DataRequired(), Length(max=1000)])


@encuesta_bp.route('/encuesta', methods=['GET', 'POST'])
def encuesta():
    form = EncuestaForm()
    mensaje = ""

    if form.validate_on_submit():
        ip_address = request.headers.get('X-Forwarded-For', request.remote_addr)
        ip_address = ip_address.split(',')[0].strip() if ip_address else '0.0.0.0'

        ahora = datetime.now()
        hace_una_hora = ahora - timedelta(hours=1)

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
            try:
                supabase.table('encuestas').insert({
                    'name': form.nombre.data,
                    'email': form.email.data,
                    'opinion': form.opinion.data,
                    'date_time': ahora.isoformat(),
                    'ip_address': ip_address
                }).execute()
                mensaje = f"¡Gracias por tu opinión, {form.nombre.data}!"
            except Exception as e:
                print("Error al insertar encuesta:", e)
                mensaje = "Hubo un error al guardar tu opinión. Intenta nuevamente."

    elif request.method == 'POST':
        mensaje = "Por favor, revisa los datos ingresados."

    return render_template('encuesta.html', titulo='Encuesta', contenido=mensaje, form=form)
