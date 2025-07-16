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
        # Si la ruta es para un archivo estático, servirlo
        if path.startswith('static/') or '.' in path:
            return send_from_directory('../static', path.split('/')[-1])
        # Si no, intentar servir el index.html (para SPA)
        return send_from_directory('../static', 'index.html')
    except Exception as e:
        app.logger.error(f"Error serving file {path}: {str(e)}")
        return jsonify({"error": "File not found"}), 404

# This is required for Vercel
def handler(event, context):
    from werkzeug.test import create_environ
    
    # Parse the event into a WSGI environment
    environ = create_environ(
        path=event.get('path', '/'),
        method=event.get('httpMethod', 'GET'),
        headers=dict(event.get('headers', {})),
        query_string=event.get('queryStringParameters', {}),
        data=event.get('body', ''),
        content_type=event.get('headers', {}).get('content-type', '')
    )
    
    # Call the app with the environment
    with app.request_context(environ):
        try:
            response = app.full_dispatch_request()
        except Exception as e:
            return {
                'statusCode': 500,
                'body': str(e)
            }
    
    # Convert the response into the format expected by Vercel
    return {
        'statusCode': response.status_code,
        'headers': dict(response.headers),
        'body': response.get_data(as_text=True)
    }

# This is needed for local development
if __name__ == '__main__':
    app.run(debug=True)