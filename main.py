from flask import Flask, render_template

app = Flask(__name__)


@app.route("/plants")
def plants():
    return render_template('plants.html', test="HBV")

@app.route("/")
def home():
    return render_template('Home.html', test="HBV")
