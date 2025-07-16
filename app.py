from flask import Flask, send_from_directory
import os

app = Flask(__name__, static_folder='static')

@app.route('/')
def home():
    return send_from_directory('static', 'index.html')

# Ruta para servir archivos estáticos
@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory('static', path)

# This is required for Vercel
def handler(event, context):
    from flask import request
    from werkzeug.wrappers import Response
    from werkzeug.test import create_environ
    
    environ = create_environ(
        path=event['path'],
        method=event['httpMethod'],
        headers=dict(event.get('headers', {})),
        query_string=event.get('queryStringParameters', {}),
        json=event.get('body')
    )
    
    with app.request_context(environ):
        response = app.full_dispatch_request()
        
    return {
        'statusCode': response.status_code,
        'headers': dict(response.headers),
        'body': response.get_data(as_text=True)
    }

if __name__ == '__main__':
    app.run(debug=True)
