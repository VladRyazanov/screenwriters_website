import os

from flask import Flask, render_template, redirect, request, abort, url_for, send_file
from flask_login import LoginManager, current_user, login_required, login_user, logout_user

import data.data_services
from data.data_services import *
from data.image_services import *
from data.script_text_services import *
from data import data_services
from forms.user import *
from forms.script import *


app = Flask(__name__, static_url_path="/static")
app.config['SECRET_KEY'] = 'secret_key'
login_manager = LoginManager()
login_manager.init_app(app)

init_database()


def abort_if_is_not_current_user(user_id):
    if user_id != current_user.id:
        abort(403)


def abort_if_current_user_is_not_author(script_id):
    if get_script_by_id(script_id)["result"].user_id != current_user.id:
        abort(403)


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


@app.route("/delete_script/<int:script_id>")
def delete_script(script_id):
    abort_if_current_user_is_not_author(script_id)
    print(data_services.delete_script(script_id))
    return redirect(f"/user/{current_user.id}/all_scripts")


@app.route('/edit_users_page/<int:user_id>', methods=['GET', 'POST'])
def edit_users_page(user_id):
    abort_if_is_not_current_user(user_id)
    form = EditUserForm()

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
        return render_template("users_page.html", user=user["result"], best_scripts=get_users_best_scripts(user["result"])["result"])


@app.route("/script/<int:script_id>")
def scripts_page(script_id):
    script = get_script_by_id(script_id)["result"]
    return render_template("script.html", script=script)


@app.route("/user/<int:user_id>/create_script", methods=['GET', 'POST'])
def create_script(user_id):
    abort_if_is_not_current_user(user_id)
    form = CreateScriptForm()
    if form.validate_on_submit():
        photo_path = save_photo_to_temporary_photos_folder(form.photo.data)
        add_new_script(user_id,
                             title=form.title.data,
                             description=form.description.data,
                             photo_path=photo_path,
                             genres=f"{form.genre.data}, {form.extra_genre.data}" if form.extra_genre.data else form.genre.data,
                             type=form.type.data,
                             text_file=form.text_file.data)
        clear_temporary_photos_folder()

        return redirect(f"/user/{user_id}")

    return render_template("create_script_page.html", form=form, title="Создание сценария")


@app.route("/edit_script/<int:script_id>", methods=['GET', 'POST'])
def edit_script(script_id):
    abort_if_current_user_is_not_author(script_id)
    form = EditScriptForm()
    if request.method == "GET":
        script = get_script_by_id(script_id)["result"]
        form.title.data = script.title
        form.description.data = script.description
        if ", " in script.genres:
            genres = script.genres.split(", ")
            form.genre.data = genres[0]
            form.extra_genre.data = genres[1]
        else:
            form.genre.data = script.genres

        form.type.data = script.type

        return render_template("create_script_page.html", form=form, title="Изменение сценария")

    if form.validate_on_submit():
        photo_path = None
        if form.photo.data:
            photo_path = save_photo_to_temporary_photos_folder(form.photo.data)

        edit_script_data(script_id,
                         form.title.data,
                         form.description.data,
                         form.type.data,
                         ", ".join([i for i in (form.genre.data, form.extra_genre.data) if i is not None]),
                         photo_path,
                         form.text_file.data)
        return redirect(f"/user/{current_user.id}")


@app.route("/user/<int:user_id>/all_scripts")
def all_users_scripts_page(user_id):
    user = get_user_by_id(user_id)["result"]
    return render_template("all_users_scripts_page.html", user=user, name_to_put_in_header=user.name)


@app.route("/script/<int:script_id>/add_review/<int:user_id>", methods=['GET', 'POST'])
def add_script_review(script_id, user_id):
    form = AddScriptReviewForm()
    if request.method == "GET":
        return render_template("add_script_review_form.html", form=form)
    if form.validate_on_submit():
        add_new_review(user_id, script_id, form.title.data, form.text.data)
        return redirect(f"/script/{script_id}")


@app.route("/script/<int:script_id>/add_mark/<int:user_id>", methods=['GET', 'POST'])
def add_script_mark(script_id, user_id):
    form = AddScriptMarkForm()
    if request.method == "GET":
        return render_template("add_script_mark_form.html", form=form)
    if form.validate_on_submit():
        add_new_mark(user_id, script_id, form.mark.data)
        return redirect(f"/script/{script_id}")


@app.route("/script/<int:script_id>/download_text")
def download_script_text(script_id):
    text_path = get_script_by_id(script_id)["result"].text_file_path
    return send_file(text_path)


@app.route("/script/<int:script_id>/all_marks")
def all_scripts_marks(script_id):
    script = get_script_by_id(script_id)["result"]
    return render_template("all_scripts_marks.html", script=script)


@app.route("/script/<int:script_id>/all_reviews")
def all_scripts_reviews(script_id):
    script = get_script_by_id(script_id)["result"]
    return render_template("all_scripts_reviews.html", script=script)


@app.route("/user/<int:user_id>/all_reviews")
def all_users_reviews(user_id):
    user = get_user_by_id(user_id)["result"]
    return render_template("all_users_reviews.html", user=user)


@app.route("/user/<int:user_id>/all_marks")
def all_users_marks(user_id):
    user = get_user_by_id(user_id)["result"]
    return render_template("all_users_marks.html", user=user)


@app.route("/user/<int:user_id>/delete_mark/<int:mark_id>")
def delete_mark(user_id, mark_id):
    data_services.delete_mark(mark_id)
    return redirect(f"/user/{user_id}/all_marks")


@app.route("/user/<int:user_id>/delete_review/<int:review_id>")
def delete_review(user_id, review_id):
    data_services.delete_review(review_id)
    return redirect(f"/user/{user_id}/all_reviews")



if __name__ == '__main__':
    app.run(port=5001)
