from flask import Flask, render_template, send_from_directory

app = Flask(__name__)

@app.route('/')
def hello():
    return render_template('index.html')

@app.route('/favicon.ico')
def favicon():
    return send_from_directory('favicon.ico')