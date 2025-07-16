from flask import Flask, send_from_directory, jsonify, request
import os
import sys
import logging

# Configurar logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = Flask(__name__, static_folder='../static')

@app.route('/<path:path>')
def serve_static(path):
    try:
        logger.debug(f"Serving static file: {path}")
        return send_from_directory('../static', path)
    except Exception as e:
        logger.error(f"Error serving file {path}: {str(e)}", exc_info=True)
        return jsonify({"error": "File not found", "path": path, "details": str(e)}), 404


# Ruta para servir archivos estáticos
@app.route('/<path:path>')
def serve_static(path):
    try:
        logger.debug(f"Serving static file: {path}")
        # Si la ruta es para un archivo estático, servirlo
        if path.startswith('static/') or '.' in path:
            return send_from_directory('../static', path.split('/')[-1])
        # Si no, intentar servir el index.html (para SPA)
        return send_from_directory('../static', 'index.html')
    except Exception as e:
        logger.error(f"Error serving file {path}: {str(e)}", exc_info=True)
        return jsonify({"error": "File not found", "path": path, "details": str(e)}), 404

# This is required for Vercel
def handler(event, context):
    from werkzeug.test import create_environ
    
    logger.debug(f"Received event: {event}")
    
    try:
        # Parse the event into a WSGI environment
        environ = create_environ(
            path=event.get('path', '/'),
            method=event.get('httpMethod', 'GET'),
            headers=dict(event.get('headers', {})),
            query_string=event.get('queryStringParameters', {}),
            data=event.get('body', ''),
            content_type=event.get('headers', {}).get('content-type', '')
        )
        
        logger.debug(f"Created WSGI environ for path: {environ.get('PATH_INFO', '/')}")
        
        # Call the app with the environment
        with app.request_context(environ):
            try:
                response = app.full_dispatch_request()
                logger.debug(f"Request processed successfully: {response.status_code}")
                return {
                    'statusCode': response.status_code,
                    'headers': dict(response.headers),
                    'body': response.get_data(as_text=True)
                }
            except Exception as e:
                logger.error(f"Error processing request: {str(e)}", exc_info=True)
                return {
                    'statusCode': 500,
                    'body': str(e),
                    'errorType': str(type(e).__name__)
                }
    except Exception as e:
        logger.error(f"Error creating WSGI environ: {str(e)}", exc_info=True)
        return {
            'statusCode': 500,
            'body': f"Internal Server Error: {str(e)}",
            'errorType': str(type(e).__name__)
        }

# This is needed for local development
if __name__ == '__main__':
    app.run(debug=True, port=5000)