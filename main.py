from flask import Flask, render_template, request, redirect, url_for, session
from login_u import add_user, request_user, request_user_avatar, request_entry, change_entry
from login_u import AccountNotFound, AccountExists
app = Flask(__name__, template_folder="templates")
app.secret_key = 'SS99PaRaDiSeScIeNcE'

@app.route('/', methods=['GET', 'POST'])
def index():
    return redirect('/home')

#Корневой каталог, используется для неавторизованного пользователя
@app.route('/home', methods=['GET', 'POST'])
def home():
    if session.get('login') == None:
        if request.method == 'POST':
            query = []
            query.append(request.form.get('Войти'))
            query.append(request.form.get('Регистрация'))
            name = list(filter(lambda x: x, query))[0]
            print(name)
            return redirect('/authorization/' + name)
        return render_template("Главная страница.html")
    else:
        return redirect(url_for('home_login', login=session['login']))

#Страница авторизации/регистрации
@app.route('/authorization/<form>', methods=['GET', 'POST'])
def authorize(form):
    if form == 'вход':
        if request.method == "POST":
            login = request.form['login']
            password = request.form['password']
            try:
                login = request_user(login, password)
            except AccountNotFound:
                return render_template('Форма входа.html', text="Неверное имя пользователя или пароль")
            change_entry(form, login=login)
            session['login'] = login
            return redirect('/home/' + login)

        return render_template('Форма входа.html')
    elif form == 'регистрация':
        if request.method == 'POST':
            login = request.form['login']
            email = request.form['email']
            password = request.form['password']
            password_check = request.form['password_check']
            if password == password_check:
                try:
                    add_user(login=login, email=email, password=password)
                except AccountExists:
                    return render_template('Форма регистрации.html', text='Аккаунт с такими данными уже существует')
                return redirect('/authorization/вход')
            else:
                return render_template("Форма регистрации.html", text="Пароли не совпадают")
    return render_template("Форма регистрации.html")


#Открытие курса.
@app.route('/courses/<course>', methods=['GET', 'POST'])
def courses(course):
    login = session.get('login')
    if request.method == "POST":
        act = []
        act.append(request.form.get('Выйти'))
        action = list(filter(lambda x: x, act))[0]
        if action == 'выход':
            print(action)
            change_entry(action, login)
            session.pop('login', None)
            return redirect('/home')
    login = session.get('login')
    if login != None:
        avatar = request_user_avatar(login)
        return render_template(course + '.html', path=avatar)
    else:
        return redirect(url_for('authorize', form='вход'))

#Главная страница с курсами, адаптированная для конкретного пользователя(аватарка, прогресс, личный кабинет)
@app.route('/home/<login>', methods=['GET', 'POST'])
def home_login(login):
    if session.get('login') != None:
        if session['login'] == login:
            avatar = request_user_avatar(login)
        else:
            return redirect(url_for('home_login', login=session['login'])) #На время, позже заменю на представление для стороннего пользователя
    else:
        return redirect(url_for('authorize', form='вход'))
    if request.method == "POST":

        action = request.form.get('Выйти')
        if action:
            change_entry(action, login)
            session.pop('login')
            return redirect('/home')
    return render_template('Главная страница вход.html', path=avatar)

app.run(debug=True)



