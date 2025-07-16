from flask import Flask, send_from_directory, jsonify, request
import os

app = Flask(__name__, static_folder='../static')

@app.route('/')
def home():
    try:
        return send_from_directory('../static', 'index.html')
    except Exception as e:
        app.logger.error(f"Error serving index.html: {str(e)}")
        return jsonify({"error": "Internal Server Error"}), 500

# Ruta para servir archivos estáticos
@app.route('/<path:path>')
def serve_static(path):
    try:
        return send_from_directory('../static', path)
    except Exception as e:
        app.logger.error(f"Error serving static file {path}: {str(e)}")
        return jsonify({"error": "File not found"}), 404

# Favicon route
@app.route('/favicon.ico')
def favicon():
    return send_from_directory('../static', 'favicon.ico'), 200, {'Content-Type': 'image/x-icon'}

# This is required for Vercel
def handler(event, context):
    import json
    from werkzeug.test import create_environ
    
    # Parse the event into a WSGI environment
    environ = create_environ(
        path=event.get('path', '/'),
        method=event.get('httpMethod', 'GET'),
        headers=dict(event.get('headers', {})),
        query_string=event.get('queryStringParameters', {}),
        data=event.get('body', ''),
        content_type=event.get('headers', {}).get('Content-Type', '')
    )
    
    # Call the app with the environment
    with app.request_context(environ):
        response = app.full_dispatch_request()
    
    # Convert the response into the format expected by Vercel
    return {
        'statusCode': response.status_code,
        'headers': dict(response.headers),
        'body': response.get_data(as_text=True)
    }

# This is needed for local development
if __name__ == '__main__':
    app.run(debug=True)