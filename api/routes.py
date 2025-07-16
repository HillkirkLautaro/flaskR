from flask import Blueprint, render_template, abort

# Crear el blueprint con el prefijo de ruta
main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    return render_template('index.html', nombre='Usuario')

@main_bp.route('/about')
def about():
    return "Esta es una demo con Flask y Supabase en Vercel."

# Manejo de errores personalizado
@main_bp.app_errorhandler(404)
def page_not_found(e):
    return "Página no encontrada", 404
