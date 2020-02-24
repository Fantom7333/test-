from flask import Flask, render_template, request, redirect, url_for
from login_u import add_user, request_user, request_entry, change_entry

app = Flask(__name__, template_folder="templates")


@app.route('/', methods=['GET', 'POST'])
def index():
    return redirect('/home')


@app.route('/home', methods=['GET', 'POST'])
def home():
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
        if request.method == "POST":
            login = request.form['login']
            password = request.form['password']
            password_valid = request_user(login)[0]
            print(password_valid)
            if password == password_valid:
                change_entry(form, login=login)
                return redirect('/home/' + login)
            else:
                return "Пароль неверный"
        return render_template('Форма входа.html')
    elif form == 'регистрация':
        if request.method == 'POST':
            login = request.form['login']
            email = request.form['email']
            password = request.form['password']
            password_check = request.form['password_check']
            if password == password_check:
                add_user(login=login, email=email, password=password)
                return redirect('/authorization/вход')
            else:
                return render_template("Форма регистрации.html", text="Пароли не совпадают")
    return render_template("Форма регистрации.html")


@app.route('/home/<login>', methods=['GET', 'POST'])
def home_login(login):
    avatar = request_user(login)[1]
    if request.method == "POST":
        try:
            action = request.form['Выйти']
        except:
            action = request.form['Курс']

        if action == 'выход':
            change_entry(action, login)
            return redirect('/home')
        elif action == 'курс':
            return render_template('урок.html', path=avatar)
    return render_template('Главная страница вход.html', path=avatar)


app.run(debug=True)
