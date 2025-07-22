
from api import create_app

# Crear la entry point de vercel
app = create_app()

if __name__ == "__main__":
    app.run(debug=True)