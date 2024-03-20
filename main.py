import os

from flask import Flask, render_template, redirect, request, abort, url_for
from flask_login import LoginManager, current_user, login_required, login_user, logout_user

from data.data_services import *
from data.image_services import *
from forms.user import *


app = Flask(__name__, static_url_path="/static")
app.config['SECRET_KEY'] = 'secret_key'
login_manager = LoginManager()
login_manager.init_app(app)

init_database()


@login_manager.user_loader
def load_user(user_id):
    result = get_user_by_id(user_id)
    if result["success"]:
        return result["result"]
    return None


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        if form.photo.data:
            path = save_photo_to_temporary_photos_folder(form.photo.data)
        else:
            path = ""
        result = add_new_user(form.name.data,
                              form.description.data,
                              path,
                              form.email.data,
                              form.password.data)

        clear_temporary_photos_folder()

        if result["success"]:
            login_user(result["result"], remember=True)
            return redirect("/")
        return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message=result["message"])
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        checking_result = check_user_data_for_logging_in(form.email.data, form.password.data)
        if checking_result["success"]:
            if checking_result["result"]:
                login_user(checking_result["result"], remember=form.remember_me.data)
                return redirect("/")
            return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
        return None
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/edit_users_page/<int:user_id>', methods=['GET', 'POST'])
def edit_user_page(user_id):
    form = EditForm()

    if request.method == "GET":
        user = get_user_by_id(user_id)["result"]
        form.name.data = user.name
        form.description.data = user.description
        form.photo.data = user.middle_photo_path
        return render_template("edit_users_page.html", form=form)
    if form.validate_on_submit():
        path = None
        if form.photo.data:
            path = save_photo_to_temporary_photos_folder(form.photo.data)
        edit_user_data(user_id, name=form.name.data, description=form.description.data, photo=path)
        return redirect(f"/user/{user_id}")


@app.route('/')
def index():
    return redirect("/1")


@app.route('/<int:page_number>')
def scripts_main_page(page_number):
    if current_user.is_authenticated:
        scripts = get_scripts_for_main_page(current_user.id, page_number)["result"]
    else:
        scripts = get_scripts_for_main_page(None, page_number)["result"]
    total_pages_count = get_main_page_pages_count()["result"]
    return render_template('index.html',
                           scripts=scripts,
                           total_pages_count=total_pages_count,
                           pages_numbers=range(max(1, page_number - 2), min(total_pages_count + 1, page_number + 3)),
                           current_page_number=page_number)


@app.route("/user/<int:user_id>")
def users_page(user_id):
    user = get_user_by_id(user_id)
    if user["success"]:
        return render_template("users_page.html", user=user["result"])


@app.route("/script/<int:script_id>")
def script_page(script_id):
    script = get_script_by_id(script_id)
    if script["success"]:
        return render_template("script.html")


if __name__ == '__main__':
    app.run()
