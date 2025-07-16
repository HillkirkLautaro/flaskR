import os
import sys

# Asegurarse de que el directorio del proyecto esté en el path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from app import app as application
    print("Successfully imported app")
except ImportError as e:
    print(f"Error importing app: {e}")
    raise

def handler(event, context):
    return app(event, context)

# Esto es necesario para el despliegue en Vercel
# Vercel buscará una variable llamada 'app' o 'application'
app = application
api = handler
