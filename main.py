from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__, template_folder="templates")


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form['Войти']
        if name == "Войти":
            pass
        else:
            pass
    return render_template("Главная страница.html")

        # email = request.form['email']
        # password = request.form['password']
        # password_check = request.form['password_check']
        # add_user(name, email, password)
        # return redirect('/users/' + name)

app.run(debug=True)