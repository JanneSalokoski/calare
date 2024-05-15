from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/")
def index():
    features = ["server", "user-interface"]
    return render_template("index.html", features=features)

@app.route("/resources")
def resources():
    return "Resources"

@app.route("/admin")
def admin():
    return "Admin control panel"

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/auth", methods=["POST"])
def auth():
    print("args:")
    for arg in request.args:
        print(arg)
    if request.form["username"] == "Admin" and request.form["password"] == "Qwerty":
        return render_template("login_success.html", username=request.form["username"])
    else:
        return render_template("login_failed.html"), 401







