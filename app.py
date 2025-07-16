from flask import Flask, send_from_directory, jsonify
import os

app = Flask(__name__, static_folder='static')

@app.route('/')
def home():
    try:
        return send_from_directory('static', 'index.html')
    except Exception as e:
        app.logger.error(f"Error serving index.html: {str(e)}")
        return jsonify({"error": "Internal Server Error"}), 500

# Ruta para servir archivos estáticos
@app.route('/<path:path>')
def serve_static(path):
    try:
        return send_from_directory('static', path)
    except Exception as e:
        app.logger.error(f"Error serving static file {path}: {str(e)}")
        return jsonify({"error": "File not found"}), 404

# Favicon route
@app.route('/favicon.ico')
def favicon():
    return app.send_static_file('favicon.ico'), 200, {'Content-Type': 'image/x-icon'}

# This is required for Vercel
def handler(event, context):
    from flask import request
    from werkzeug.wrappers import Response
    from werkzeug.test import create_environ
    
    try:
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
    except Exception as e:
        return {
            'statusCode': 500,
            'body': str(e)
        }

# This is needed for Vercel
app = app

if __name__ == '__main__':
    app.run(debug=True)
