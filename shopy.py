from flask import Flask, render_template # Basic config, Render templates
from flask import url_for # So we dont need to worry to import which file

app = Flask(__name__)


@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')

@app.route("/register")
def register():
    return render_template('register.html')
@app.route("/login")
def login():
    return render_template('login.html')


if __name__ == "__main__":
    app.run()
