from flask import Flask, render_template, request, redirect, url_for
from login_u import add_user

app = Flask(__name__, template_folder="templates")


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        try:
            name = request.form["Войти"]
        except:
            name = request.form["Регистрация"]
        print(name)
        return redirect('/authorization/' + name)
    return render_template("Главная страница.html")


@app.route('/authorization/<form>', methods=['GET', 'POST'])
def authorize(form):
    if form == 'вход':
        return render_template('Форма входа.html')
    elif form == 'регистрация':
        if request.method == 'POST':
            login = request.form['login']
            email = request.form['email']
            password = request.form['password']
            password_check = request.form['password_check']
            if password == password_check:
                add_user(login, email, password)
                return render_template("Главная страница.html")
            else:
                return render_template("Форма регистрации.html", text="Пароли не совпадают")
    return render_template('Форма регистрации.html')



app.run(debug=True)