from flask import Blueprint, render_template, abort

# Crear el blueprint con el prefijo de ruta
main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    return render_template('index.html', nombre='Usuario')

@main_bp.route('/about')
def about():
    return render_template('about.html', titulo='Acerca de', contenido="Esta es una demo con Flask y Supabase en Vercel.")


@main_bp.route('/encuesta')
def encuesta():
    return render_template('encuesta.html', titulo='Encuesta', contenido="Por favor, completa la encuesta para ayudarnos a mejorar.")

# Manejo de errores personalizado
@main_bp.app_errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404
