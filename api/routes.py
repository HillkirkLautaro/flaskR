from flask import Blueprint, render_template, abort, request

# Crear el blueprint con el prefijo de ruta
main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    return render_template('index.html', nombre='Usuario')

@main_bp.route('/about')
def about():
    return render_template('about.html', titulo='Acerca de', contenido="Esta es una demo con Flask y Supabase en Vercel.")


@main_bp.route('/encuesta', methods=['GET', 'POST'])
def encuesta():
    if request.method == 'POST':
        # Procesar datos del formulario aquí
        nombre = request.form.get('nombre')
        email = request.form.get('email')
        opinion = request.form.get('opinion')
        # Puedes guardar, mostrar o procesar estos datos
        mensaje = "¡Gracias por tu opinión, {}!".format(nombre)
        return render_template('encuesta.html', titulo='Encuesta', contenido=mensaje)
    return render_template('encuesta.html', titulo='Encuesta', contenido="Por favor, completa la encuesta para ayudarnos a mejorar.")
