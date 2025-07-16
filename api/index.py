from .app import app as application

def handler(event, context):
    return application(event, context)

# Variables necesarias para Vercel
app = application
api = handler
