from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from login_u import add_user, request_user, request_user_avatar, request_entry, change_entry, add_check_password, \
remove_check_password, get_check_password, change_user_password, check_user_by_email, request_user_login, \
get_sections, get_courses, get_classes, get_parts_of_class
from login_u import AccountNotFound, AccountExists, CourseNotFound, SectionNotFound,  ClassNotFound
from flask_mail import Mail, Message
import subprocess
from werkzeug.security import generate_password_hash, check_password_hash
import requests
from flask_marshmallow import Marshmallow
from str_functions import for_display


app = Flask(__name__, template_folder="templates")

app.secret_key = "FIYGRFERBKCYBKEUYVCYECERUYBCRU"
#Secret_key из переменной окружение моего ноутбука
# app.secret_key = str(subprocess.check_output(['launchctl', 'getenv', 'SECRET_KEY']))[2:-3]


mail = Mail(app)
ma = Marshmallow(app)

class Courses_m(ma.Schema):
    class Meta:
        fields = ('course_name', 'avatar')

courses_m = Courses_m(many=True)


class Sections_m(ma.Schema):
    class Meta:
        fields = ('section_name', 'avatar')

sections_m = Sections_m(many=True)


class Classes_m(ma.Schema):
    class Meta:
        fields = ('class_name', 'avatar')

classes_m = Classes_m(many=True)

class Parts_Of_Class_m(ma.Schema):
    class Meta:
        fields = ('info', 'avatar', 'test', 'valid_id')

parts_of_class_m = Parts_Of_Class_m(many=True)



print( 'secret_key: ' + str(app.secret_key))



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



@app.route('/courses/<course>', methods=["GET"])
def courses(course):
    login = session.get('login')
    if login:
        try:
            sections = get_sections(course)
        except CourseNotFound:
            return redirect(url_for('home'))
        result = sections_m.dump(sections)
        for i in result:
            i['section_name_display'] = for_display(i['section_name'])
        print(result)
        return jsonify(result)
    else:
        return redirect(url_for('authorize', form="вход"))


@app.route('/courses/<course>/<section>', methods=["GET"])
def sections(course, section):
    login = session.get('login')
    if login:
        try:
            classes = get_classes(course, section)
        except CourseNotFound:
            return redirect(url_for('home_login', login=login))
        except SectionNotFound:
            return redirect(url_for('courses', course=course))
        result = classes_m.dump(classes)
        for i in result:
            i['class_name_display'] = for_display(i['class_name'])
        print(result)
        return jsonify(result)
    else:
        return redirect(url_for('authorize', form="вход"))


@app.route('/courses/<course>/<section>/<class_name>', methods=["GET"])
def classes(course, section, class_name):
    login = session.get('login')
    if login:
        try:
            parts_of_class = get_parts_of_class(course, section, class_name=class_name)
        except CourseNotFound:
            return redirect(url_for('home_login', login=login))
        except SectionNotFound:
            return redirect(url_for('courses', course=course))
        except ClassNotFound:
            return redirect(url_for('sections', course=course, section=section))

        result = parts_of_class_m.dump(parts_of_class)
        for i in result:
            if i['test']:
                info = i['info']
                info_title = info[:info.find(':')+1]
                info_text = info[len(info_title)-1:]
                i['info_title'] = info_title
                info_text = info_text.split(', ')
                i['info_text'] = info_text
                del i['info']
            else:
                del i['valid_id']
        print(result)
        return jsonify(result)
    else:
        return redirect(url_for('authorize', form="вход"))

@app.route('/<email>/confirm_new_password', methods=['GET', 'POST'])
def confirm(email):
    code_valid = get_check_password(email)

    if request.method == "POST":
        code = request.form['code']
        login = request_user_login(email)
        old_password = request_user(login)[1]
        print(old_password)
        new_password = request.form['password']
        bool_hash = check_password_hash(old_password, new_password)
        print(bool_hash)
        if code_valid == code:
            if bool_hash:
                return render_template("confirm.html", error='Old eq New')
            else:
                change_user_password(email, new_password)
                remove_check_password(email)
                login = request_user_login(email)
                session['login'] = login
                return redirect(url_for('home_login', login=login))
        else:
            return render_template('confirm.html', error='Code not valid')

    if request.referrer == "http://127.0.0.1:5000/forgot" and code_valid:
        return render_template("confirm.html", error=False)
    else:
        return redirect(url_for('forgot'))

#Страница запроса восстановления пароля
@app.route('/forgot', methods=['GET', 'POST'])
def forgot():
    if request.method == "POST":
        email = request.form['email']
        try:
            email = check_user_by_email(email)
        except AccountNotFound:
            return render_template('forgot.html', error=True)
        code = add_check_password(email)
        msg = Message("Код подтверждения", recipients=[email])
        msg.body = code
        mail.send(msg)
        return redirect(f'/{email}/confirm_new_password')

    return render_template('forgot.html', error=False)
#Страница авторизации/регистрации
@app.route('/authorization/<form>', methods=['GET', 'POST'])
def authorize(form):
    if form == 'вход':
        if request.method == "POST":
            act = []
            act.append(request.form.get('Войти'))
            act.append(request.form.get('Забыл пароль'))
            action = list(filter(lambda x: x, act))[0]
            if action == "Войти":
                login = request.form['login']
                password = request.form['password']
                try:
                    login, password_hash_valid = request_user(login)
                    bool_hash = check_password_hash(password_hash_valid, password)
                except AccountNotFound:
                    return render_template('Форма входа.html', text="Неверное имя пользователя или пароль")
                if bool_hash:
                    change_entry(form, login=login)
                    session['login'] = login
                else:
                    return render_template('Форма входа.html', text="Неверное имя пользователя или пароль")
                return redirect('/home/' + login)
            elif action == "Забыл пароль":
                return redirect('/forgot')
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






