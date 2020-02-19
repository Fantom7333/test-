from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__, template_folder="templates")


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template("Главная страница.html")
app.run(debug=True)