from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "Hello World! <strong>Funcionou </strong>", 200

app.run(debug=True, use_reloader=True)
