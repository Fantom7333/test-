from flask import Flask, render_template, request, redirect, url_for
from login_u import add_user, request_user, request_entry, change_entry, set_auth_attr, get_login


app = Flask(__name__, template_folder="templates")


@app.route('/', methods=['GET', 'POST'])
def index():
    oz = request_entry()
    if oz == 0:
        if request.method == 'POST':
            try:
                name = request.form["Войти"]
            except:
                name = request.form["Регистрация"]
            print(name)
            return redirect('/authorization/' + name)
        return render_template("Главная страница.html")
    else:
        if request.method == 'POST':
            name = request.form['Выйти']
            change_entry(name)
            render_template("Главная страница.html")
        avatar = request_user(get_login())[1]
        return render_template("Главная страница вход.html", path = avatar)

@app.route('/authorization/<form>', methods=['GET', 'POST'])
def authorize(form):
    if form == 'вход':
        if request.method == "POST":
            login = request.form['login']
            password = request.form['password']
            password_valid = request_user(login)[0]
            if password == password_valid:
                change_entry(form)
                set_auth_attr(login=login)
                print(request_entry())
                return redirect('/')
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
    return render_template('Форма регистрации.html')
app.run(debug=True)