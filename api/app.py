from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def hello():
    return "<h1>hello flaskR</h1>"

# Esto es necesario para Vercel
handler = app

if __name__ == '__main__':
    app.run(debug=True, port=5000)