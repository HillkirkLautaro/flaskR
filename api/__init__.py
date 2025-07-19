import os
from flask import Flask

def create_app():
    # Obtener la ruta al directorio actual
    static_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static')
    # Definir la ruta al directorio de plantillas
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # Definir la ruta al directorio de plantillas
    template_dir = os.path.join(current_dir, 'template')

    # Crear la aplicación Flask
    app = Flask(__name__, 
               template_folder=template_dir,
               static_folder='static')

    # Registrar blueprints
    from .routes import main_bp
    app.register_blueprint(main_bp)

    return app
