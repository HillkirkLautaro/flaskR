from flask import Flask, send_from_directory, jsonify

app = Flask(__name__, static_folder='../static', static_url_path='')

# Ruta para la página principal
@app.route('/')
def index():
    return send_from_directory('../static', 'index.html')

# Ruta para manejar archivos estáticos
@app.route('/<path:path>')
def serve_static(path):
    # Si la ruta es un archivo estático (tiene extensión)
    if '.' in path:
        try:
            return send_from_directory('../static', path)
        except:
            return jsonify({"error": "File not found"}), 404
    # Para cualquier otra ruta, servir index.html (SPA)
    return send_from_directory('../static', 'index.html')

# Esto es necesario para que Vercel pueda importar la aplicación
# sin ejecutar el servidor de desarrollo
if __name__ == '__main__':
    app.run(debug=True, port=5000)

# Este es el objeto que Vercel espera
handler = app