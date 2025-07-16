from flask import Flask

@app.route('/')
def hello():
    return "<h1>hello flaskR</h1>"

@app.route('/favicon.ico')
def favicon():
    return send_from_directory('favicon.ico')