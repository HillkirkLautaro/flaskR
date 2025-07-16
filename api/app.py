from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    return "<h1>hello flaskR</h1>"

@app.route('/favicon.ico')
def favicon():
    return send_from_directory('static', 'favicon.ico')