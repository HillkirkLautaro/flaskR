import os
from flask import Flask

def create_app():

    # Definir la ruta al directorio de plantillas y estáticos
    current_dir = os.path.dirname(os.path.abspath(__file__))
    template_dir = os.path.join(current_dir, 'templates')
    static_dir = os.path.join(current_dir, 'static')

    # Crear la aplicación Flask
    app = Flask(__name__, 
               template_folder=template_dir,
               static_folder=static_dir)

    # Registrar blueprints
    from .routes import main_bp
    app.register_blueprint(main_bp)

    return app
