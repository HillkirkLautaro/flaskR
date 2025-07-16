from flask import Flask, send_from_directory, jsonify

app = Flask(__name__, static_folder='../static', static_url_path='/static')

# Ruta para SPA, que sirve index.html para todas las rutas que no sean archivos estáticos
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    if path != "" and ('.' in path or path.startswith('static/')):
        # Intentar servir archivo estático
        try:
            return send_from_directory('../static', path)
        except Exception:
            return jsonify({"error": "File not found"}), 404
    else:
        # Servir index.html para que la SPA maneje el routing
        return send_from_directory('../static', 'index.html')


if __name__ == '__main__':
    app.run(debug=True, port=5000)
