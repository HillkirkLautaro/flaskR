import os
import sys

# Asegurarse de que el directorio del proyecto esté en el path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from app import app, handler
    print("Successfully imported app and handler")
except ImportError as e:
    print(f"Error importing app or handler: {e}")
    raise

def vercel_handler(event, context):
    try:
        print(f"Vercel handler called with event: {event}")
        return handler(event, context)
    except Exception as e:
        print(f"Error in vercel_handler: {e}")
        return {
            'statusCode': 500,
            'body': f'Internal Server Error: {str(e)}',
            'headers': {
                'Content-Type': 'application/json'
            }
        }

# This is the entry point for Vercel
# Vercel buscará una función llamada 'app' o 'api' por defecto
# También podemos usar la configuración en vercel.json para especificar la función de entrada
app = app
api = vercel_handler
