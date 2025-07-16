import os
from flask import Flask

def create_app():
    # Obtener la ruta al directorio actual
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Verificar si estamos en producción (Vercel)
    if 'VERCEL' in os.environ:
        # En producción, las plantillas están en el mismo directorio
        template_dir = os.path.join(current_dir, 'template')
    else:
        # En desarrollo, usar la ruta relativa estándar
        template_dir = os.path.join(current_dir, 'template')
    
    # Crear la aplicación Flask
    app = Flask(__name__, 
               template_folder=template_dir,
               static_folder='static')

    # Registrar blueprints
    from .routes import main_bp
    app.register_blueprint(main_bp)

    return app
