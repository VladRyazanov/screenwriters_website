from flask import Flask, render_template, redirect, request, abort, send_file
from flask_login import LoginManager, current_user, login_required, login_user, logout_user
from flask_restful import Api

from data import data_services
from data import user_resource
from data.data_services import *
from data.image_services import *
from forms.script import *
from forms.user import *

# создание приложения
app = Flask(__name__, static_url_path="/static")
app.config['SECRET_KEY'] = 'secret_key'
# создание api
api = Api(app)
api.add_resource(user_resource.UserListResource, '/api/v2/users')
api.add_resource(user_resource.UserResource, '/api/v2/users/<int:users_id>')
# создание login_manager
login_manager = LoginManager()
login_manager.init_app(app)


def abort_if_current_user_is_not_author(script_id):
    # Функция для вызова ошибки, если пользователь не является автором сценария.
    # Используется, когда происходит переход на страницу редактирования сценария
    if get_script_by_id(script_id).user_id != current_user.id:
        abort(403)


@login_manager.user_loader
def load_user(user_id):
    return get_user_by_id(user_id)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        # Проверка пароля
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        # Проверка наличия пользователя с введённым email
        if check_if_user_with_this_email_already_exists(form.email.data):
            return render_template('register.html',
                                   form=form, message="Пользователь с таким email уже существует")

        # Сохраняем фото во временную папку
        path = save_photo_to_temporary_photos_folder(form.photo.data)
        # Создаем пользователя
        add_new_user(form.name.data,
                     form.description.data,
                     path,
                     form.email.data,
                     form.password.data)
        return redirect("/login")

    return render_template('register.html', title='Регистрация', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # Проверка введённых данных
        checking_result = check_user_data_for_logging_in(form.email.data, form.password.data)
        if checking_result:
            login_user(checking_result, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)

    return render_template('login.html', title='Авторизация', form=form)


@app.route("/delete_script/<int:script_id>")
@login_required
def delete_script(script_id):
    # Удаление сценария
    abort_if_current_user_is_not_author(script_id)
    print(data_services.delete_script(script_id))
    return redirect(f"/user/{current_user.id}/all_scripts")


@app.route('/edit_users_page/<int:user_id>', methods=['GET', 'POST'])
@login_required
def edit_users_page(user_id):
    # Редактирования страницы пользователя
    form = EditUserForm()
    if request.method == "GET":
        user = get_user_by_id(user_id)
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
    # Главная страница
    if current_user.is_authenticated:
        # Если пользователь авторизован, то загружаем сценарии, отсортированные по его подпискам, просмотрам и т.д.
        scripts = get_scripts_for_main_page(current_user.id, page_number)
    else:
        scripts = get_scripts_for_main_page(None, page_number)
    # Узнаем количество страниц
    total_pages_count = get_main_page_pages_count()
    return render_template('index.html',
                           scripts=scripts,
                           total_pages_count=total_pages_count,
                           pages_numbers=range(max(1, page_number - 2), min(total_pages_count + 1, page_number + 3)),
                           current_page_number=page_number)


@app.route("/user/<int:user_id>")
def users_page(user_id):
    # Страница пользователя
    user = get_user_by_id(user_id)
    return render_template("users_page.html", user=user, best_scripts=get_users_best_scripts(user))


@app.route("/script/<int:script_id>")
def scripts_page(script_id):
    # Страница сценария
    script = get_script_by_id(script_id)
    if current_user.is_authenticated:
        # Если пользователь авторизован, добавляем сценарий в просмотренные
        add_script_to_viewed_scripts(current_user.id, script.id)
    return render_template("script.html", script=script)


@app.route("/user/<int:user_id>/create_script", methods=['GET', 'POST'])
@login_required
def create_script(user_id):
    # Создание сценария
    form = CreateScriptForm()
    if form.validate_on_submit():
        # Сохранение фото во временную папку
        photo_path = save_photo_to_temporary_photos_folder(form.photo.data)
        add_new_script(user_id,
                       title=form.title.data,
                       description=form.description.data,
                       photo_path=photo_path,
                       genres=f"{form.genre.data}, {form.extra_genre.data}"
                       if form.extra_genre.data else form.genre.data,
                       type=form.type.data,
                       text_file=form.text_file.data)
        clear_temporary_photos_folder()

        return redirect(f"/user/{user_id}")

    return render_template("create_script_page.html", form=form, title="Создание сценария")


@app.route("/edit_script/<int:script_id>", methods=['GET', 'POST'])
@login_required
def edit_script(script_id):
    # Редактирование сценария
    abort_if_current_user_is_not_author(script_id)
    form = EditScriptForm()
    if request.method == "GET":
        script = get_script_by_id(script_id)
        form.title.data = script.title
        form.description.data = script.description
        # Отображение жанров
        if ", " in script.genres:
            genres = script.genres.split(", ")
            form.genre.data = genres[0]
            form.extra_genre.data = genres[1]
        else:
            form.genre.data = script.genres

        form.type.data = script.type

        return render_template("create_script_page.html", form=form, title="Изменение сценария")

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
    user = get_user_by_id(user_id)
    return render_template("all_users_scripts_page.html", user=user, name_to_put_in_header=user.name)


@app.route("/script/<int:script_id>/add_review/<int:user_id>", methods=['GET', 'POST'])
@login_required
def add_script_review(script_id, user_id):
    # Добавление рецензии
    form = AddScriptReviewForm()
    if request.method == "GET":
        return render_template("add_script_review_form.html", form=form)
    if form.validate_on_submit():
        add_new_review(user_id, script_id, form.title.data, form.text.data)
        return redirect(f"/script/{script_id}")


@app.route("/script/<int:script_id>/add_mark/<int:user_id>", methods=['GET', 'POST'])
@login_required
def add_script_mark(script_id, user_id):
    # Добавление оценки
    form = AddScriptMarkForm()
    if request.method == "GET":
        return render_template("add_script_mark_form.html", form=form)
    if form.validate_on_submit():
        add_new_mark(user_id, script_id, float(form.mark.data))
        return redirect(f"/script/{script_id}")


@app.route("/user/<int:user_id>/delete_mark/<int:mark_id>")
@login_required
def delete_mark(user_id, mark_id):
    # Удаление оценки
    data_services.delete_mark(mark_id)
    return redirect(f"/user/{user_id}/all_marks")


@app.route("/user/<int:user_id>/delete_review/<int:review_id>")
@login_required
def delete_review(user_id, review_id):
    # Удаление комментария
    data_services.delete_review(review_id)
    return redirect(f"/user/{user_id}/all_reviews")


@app.route("/script/<int:script_id>/download_text")
def download_script_text(script_id):
    # Скачивание текста
    text_path = get_script_by_id(script_id).text_file_path
    return send_file(text_path)


@app.route("/script/<int:script_id>/all_marks")
def all_scripts_marks(script_id):
    # Просмотр всех оценок сценария
    script = get_script_by_id(script_id)
    return render_template("all_scripts_marks.html", script=script)


@app.route("/script/<int:script_id>/all_reviews")
def all_scripts_reviews(script_id):
    # Просмотр всех рецензий на сценарий
    script = get_script_by_id(script_id)
    return render_template("all_scripts_reviews.html", script=script)


@app.route("/user/<int:user_id>/all_reviews")
def all_users_reviews(user_id):
    # Просмотр всех рецензий пользователя
    user = get_user_by_id(user_id)
    return render_template("all_users_reviews.html", user=user)


@app.route("/user/<int:user_id>/all_marks")
def all_users_marks(user_id):
    # Просмотр всех оценок пользователя
    user = get_user_by_id(user_id)
    return render_template("all_users_marks.html", user=user)


@app.route("/logout")
def logout():
    # Выход из аккаунта
    logout_user()
    return redirect("/")


@app.route("/subscribe/<int:target_id>")
@login_required
def subscribe(target_id):
    # Подписка одного пользователя на другого
    make_user_subscriber_of_another_user(current_user.id, target_id)
    return redirect(f"/user/{target_id}")


@app.route("/unsubscribe/<int:target_id>")
def unsubscribe(target_id):
    # Отписка одного пользователя от другого
    unsubscribe_user_from_another_user(current_user.id, target_id)
    return redirect(f"/user/{target_id}")


if __name__ == '__main__':
    app.run(port=5001)
