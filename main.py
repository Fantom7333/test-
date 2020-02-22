from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__, template_folder="templates")


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        try:
            name = request.form["Войти"]
        except:
            name = request.form["Регистрация"]
        print(name)
    return render_template("Главная страница.html")
app.run(debug=True)