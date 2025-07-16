from flask import Flask, render_template, send_from_directory
app = Flask(__name__, template_folder="template", static_folder="static")

@app.route('/')
def hello():
    return render_template("index.html")

@app.route('/favicon.ico')
def favicon():
    return send_from_directory("static", "favicon.ico")


if __name__ == "__main__":
    app.run(debug=True, port=5000)