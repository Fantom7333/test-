from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from login_u import add_user, request_user, request_user_avatar, request_entry, change_entry, add_check_password, \
remove_check_password, get_check_password, change_user_password, check_user_by_email, request_user_login, \
get_sections, get_courses, get_classes, get_parts_of_class, request_user_obj
from login_u import AccountNotFound, AccountExists, CourseNotFound, SectionNotFound,  ClassNotFound
from flask_mail import Mail, Message
import subprocess
from werkzeug.security import generate_password_hash, check_password_hash
import requests
from flask_marshmallow import Marshmallow
from str_functions import for_display
from flask_cors import CORS

app = Flask(__name__, template_folder="templates")
CORS(app)

app.secret_key = "FIYGRFERBKCYBKEUYVCYECERUYBCRU"
#Secret_key из переменной окружение моего ноутбука
# app.secret_key = str(subprocess.check_output(['launchctl', 'getenv', 'SECRET_KEY']))[2:-3]


mail = Mail(app)
ma = Marshmallow(app)


class User_m(ma.Schema):
    class Meta:
        fields = ('login', 'avatar')

user_m = User_m(many=False)

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

print('secret_key: ' + str(app.secret_key))




#Корневой каталог, используется для неавторизованного пользователя
@app.route('/', methods=['GET'])
def home():
    courses = get_courses()
    result = courses_m.dump(courses)
    return jsonify(result)



@app.route('/<course>', methods=["GET"])
def courses(course):
    try:
        sections = get_sections(course)
    except CourseNotFound:
        return jsonify({'redirect': "/"})
    result = sections_m.dump(sections)
    for i in result:
        i['section_name_display'] = for_display(i['section_name'])
    print(result)
    return jsonify(result)



@app.route('/<course>/<section>', methods=["GET"])
def sections(course, section):
    try:
        classes = get_classes(course, section)
    except CourseNotFound:
        return jsonify({'redirect': '/'})
    except SectionNotFound:
        return jsonify({'redirect': f'/{course}'})
    result = classes_m.dump(classes)
    for i in result:
        i['class_name_display'] = for_display(i['class_name'])
    print(result)
    return jsonify(result)




@app.route('/<course>/<section>/<class_name>', methods=["GET"])
def classes(course, section, class_name):
        try:
            parts_of_class = get_parts_of_class(course, section, class_name=class_name)
        except CourseNotFound:
            return jsonify({'redirect': '/'})
        except SectionNotFound:
            return jsonify({'redirect': f'/{course}'})
        except ClassNotFound:
            return jsonify({'redirect': f'/{course}/{section}'})
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



#Страница авторизации/регистрации/восстановления пароля/подтверждения нового пароля
@app.route('/authorization/<form>', methods=['POST'])
def post(form):
        if form == "log_in":
            login = request.json['login']
            password = request.json['password']
            try:
                login, password_hash_valid = request_user(login)
                bool_hash = check_password_hash(password_hash_valid, password)
            except AccountNotFound:
                return jsonify({"error": True})
            if bool_hash:
                change_entry(form, login=login)
                session['login'] = login
                return jsonify({'error': False})
            else:
                return jsonify({"error": True})


        elif form == "sign_up":

            login = request.json['login']
            email = request.json['email']
            password = request.json['password']
            try:
                add_user(login=login, email=email, password=password)
            except AccountExists:
                return jsonify({"error": True})
            return jsonify({"error": False})


        elif form == "forgot":
            email = request.json['email']
            try:
                email = check_user_by_email(email)
            except AccountNotFound:
                return jsonify({"error": True})
            code = add_check_password(email)
            msg = Message("Код подтверждения", recipients=[email])
            msg.body = code
            mail.send(msg)
            session["mail_confirm"] = email
            return jsonify({"error": False})

        elif form == "confirm_new_password":
            email = session.get('email_new_confirm')
            if email:
                code_valid = get_check_password(email)
                code = request.json("code")
                login = request_user_login(email)
                old_password = request_user(login)[1]
                print(old_password)
                new_password = request.form['password']
                bool_hash = check_password_hash(old_password, new_password)
                print(bool_hash)
                if code_valid == code:
                    if bool_hash:
                        return jsonify({'error': "Пароли совпадают"})
                    else:
                        change_user_password(email, new_password)
                        remove_check_password(email)
                        login = request_user_login(email)
                        session['login'] = login
                        return jsonify({'error': False})
                else:
                    return jsonify({'error': "Код подтверждения неверный"})





@app.route('/authorization/<form>', methods=["GET"])
def display(form):
    if form == "log_in":
        result = {}
        fields_name = ["login", "password"]
        fields_label = ["Логин", "Пароль"]
        fields_types = ["text", "password"]
        fields_min_lenght = ["6", "6"]
        fields_max_lenght = ["15", "20"]
        fields = list(zip(fields_name, fields_max_lenght, fields_types, fields_min_lenght, fields_max_lenght))
        print(fields)
        # Получаем список словарей с атрибутами полей.
        result['fields'] = []
        for i in fields:
            fields_new = {}
            fields_new['field_name'] = i[0]
            fields_new['field_label'] = i[1]
            fields_new['field_type'] = i[2]
            fields_new['field_min_length'] = i[3]
            fields_new['field_max_length'] = i[4]
            result['fields'].append(fields_new)

        result['fields'] = fields
        result['submit_button'] = 'Войти'
        result['bottom_label'] = "Нет аккаунта?"
        result["bottom_url"] = "/authorization/sign_un"
        result["bottom_button_value"] = "Зарегистрироваться"
        result["additional_button"] = "Забыл пароль"
        result["additional_url"] = "/authorization/forgot"
        result["redirect"] = False
        return jsonify(result)
    elif form == "sign_up":
        result = {}
        fields_name = ["login", "email", "password", "password_сheck"]
        fields_label = ["Логин", "Email", "Пароль", "Повторите пароль"]
        fields_types = ["text", "email", "password", "password"]
        fields_min_lenght = ["6", "6", "6", "6"]
        fields_max_lenght = ["15", "25", "20", "20"]
        fields = list(zip(fields_name, fields_label, fields_types, fields_min_lenght, fields_max_lenght))
        #Получаем список словарей с атрибутами полей.
        result['fields'] = []
        for i in fields:
            fields_new = {}
            fields_new['field_name'] = i[0]
            fields_new['field_label'] = i[1]
            fields_new['field_type'] = i[2]
            fields_new['field_min_length'] = i[3]
            fields_new['field_max_length'] = i[4]
            result['fields'].append(fields_new)

        result['submit_button'] = 'Зарегистрироваться'
        result['bottom_label'] = "Есть аккаунт?"
        result["bottom_url"] = "/authorization/log_in"
        result["bottom_button_value"] = "Войти"
        result["additional_button"] = False
        result["additional_url"] = False
        result["redirect"] = False
        return jsonify(result)

    elif form == "forgot":
        result = {}
        fields_name = ["email"]
        fields_label = ["Email"]
        fields_types = ["email"]
        fields_min_lenght = ["6"]
        fields_max_lenght = ["25"]
        fields = list(zip(fields_name, fields_label, fields_types, fields_min_lenght, fields_max_lenght))
        # Получаем список словарей с атрибутами полей.
        result['fields'] = []
        for i in fields:
            fields_new = {}
            fields_new['field_name'] = i[0]
            fields_new['field_label'] = i[1]
            fields_new['field_type'] = i[2]
            fields_new['field_min_length'] = i[3]
            fields_new['field_max_length'] = i[4]
            result['fields'].append(fields_new)
        result['fields'] = fields
        result['submit_button'] = "Отправить код"
        result['bottom_label'] = False
        result["bottom_url"] = False
        result["bottom_button_value"] = False
        result["additional_button"] = False
        result["additional_url"] = False
        result["redirect"] = False

    elif form == "confirm_new_password":
        result = {}
        fields_name = ["email", "code"]
        fields_label = ["email", "Код подтверждения"]
        fields_types = ["email", "text"]
        fields_min_lenght = ["6", "10"]
        fields_max_lenght = ["25", "10"]
        fields = zip(fields_name, fields_types, fields_min_lenght, fields_max_lenght)
        # Получаем список словарей с атрибутами полей.
        result['fields'] = []
        for i in fields:
            fields_new = {}
            fields_new['field_name'] = i[0]
            fields_new['field_label'] = i[1]
            fields_new['field_type'] = i[2]
            fields_new['field_min_length'] = i[3]
            fields_new['field_max_length'] = i[4]
            result['fields'].append(fields_new)

        result['fields'] = fields
        result['submit_button'] = "Сменить пароль"
        result['bottom_label'] = False
        result["bottom_url"] = False
        result["bottom_button_value"] = False
        result["additional_button"] = False
        result["additional_url"] = False
        result["redirect"] = False



# @app.route('/authorization/log_in', methods=["GET"])
# def login():

app.run(debug=True)






