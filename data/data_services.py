from constants import TYPES_OF_USERS_PHOTOS_AND_SIZES, TYPES_OF_SCRIPTS_PHOTOS_AND_SIZES
from data import db_session
from data.image_services import *
from data.script import Script
from data.script_mark import ScriptMark
from data.script_review import ScriptReview
from data.script_text_services import *
from data.user import User

"""
Файл, где расположены все функции для взаимодействия с базой данных программы
"""

# Инициализация базы данных
db_session.global_init("db/data.db")
db_sess = db_session.create_session()


# Служебные функции
# Функции, которые используются только в других функциях этого файла


def get_user_attribute_value(user_id, attribute_name):
    # функция для получения значения аттрибута объекта класса User
    # Используется в функциях для получения оценок, рецензий, сценариев пользователя
    user = db_sess.get(User, user_id)
    return list(getattr(user, attribute_name))


def get_script_attribute_value(script_id, attribute_name):
    # Функция для получения значения аттрибута у объекта класса Script
    script = db_sess.get(Script, script_id)
    return getattr(script, attribute_name)


# Функции для пользователей


#
def add_new_user(name, description, photo_path, email, password):
    # Фунцкия добавления пользователя
    # Создание нового пользователя
    new_user = User(name=name,
                    description=description,
                    email=email)
    # Установка пароля
    new_user.set_password(password)
    # Добавление нового пользователя в базу данных
    db_sess.add(new_user)
    db_sess.commit()
    # Установка фотографии для этого пользователя
    set_photo_for_object(new_user, photo_path, TYPES_OF_USERS_PHOTOS_AND_SIZES)
    db_sess.commit()
    # Возвращение созданного объекта
    return get_user_by_id(new_user.id)


def check_if_user_with_this_email_already_exists(email):
    # Функция для проверки наличия пользователя с заданной почтой
    # Используется для регистрации пользователей
    if db_sess.query(User).filter(User.email == email).first():
        return True
    return False


def edit_user_data(user_id, name, description, photo):
    # Функция редактирования данных на страницу пользователя
    user = db_sess.get(User, user_id)
    user.name = name
    user.description = description
    # Если новое фото профиля было приложено, то устанавливаем его
    if photo:
        set_photo_for_object(user, photo, TYPES_OF_USERS_PHOTOS_AND_SIZES)
    db_sess.commit()


def check_user_data_for_logging_in(email, password):
    # Функция проверки данных для входа
    # Проверяет, корректность почты и пароля. используется при авторизации
    user = db_sess.query(User).filter(User.email == email).first()
    if user and user.check_password(password):
        return user
    return False


def delete_user(user_id):
    user = db_sess.get(User, user_id)
    # получение всего, что связано с пользователем
    all_user_scripts = get_user_scripts(user_id)
    all_user_marks = get_all_users_given_script_marks(user_id)
    all_user_reviews = get_all_users_given_script_reviews(user_id)
    # удаление фото
    user_photo_directory = f"static/images/users/{user.id}"
    if os.path.exists(user_photo_directory):
        previous_photos = os.listdir(user_photo_directory)
        for photo_to_remove in previous_photos:
            file_path = os.path.join(user_photo_directory, photo_to_remove)
            os.remove(file_path)
    # удаление сценариев
    for script in all_user_scripts:
        delete_script(script.id)
    # удаление оценок
    for mark in all_user_marks:
        delete_mark(mark.id)
    # удаление рецензий
    for review in all_user_reviews:
        delete_review(review.id)

    # удаляем самого пользователя и подтверждаем совершенные операции
    db_sess.delete(user)
    db_sess.commit()


def get_user_by_id(user_id):
    # Получение пользователя по id
    user = db_sess.get(User, user_id)
    return user


def get_all_users():
    # Получение всех пользователей
    all_users = db_sess.query(User).all()
    return list(all_users)


# Функции для сценариев

def add_new_script(author_user_id, title, description, photo_path, type, genres, text_file):
    # Функция для добавления сценария
    user = db_sess.get(User, author_user_id)
    new_script = Script(title=title,
                        description=description,
                        type=type,
                        genres=genres,
                        text_file_path="",
                        author=user)
    db_sess.add(new_script)
    db_sess.commit()
    # Установка текстового файла и фото
    set_script_file_for_script(new_script, text_file)
    set_photo_for_object(new_script, photo_path, TYPES_OF_SCRIPTS_PHOTOS_AND_SIZES)
    db_sess.commit()


def delete_script(script_id):
    # Функция для удаления сценария
    script = db_sess.get(Script, script_id)
    scripts_photos = os.listdir(f"static/images/scripts/{script_id}")
    # Удаления фото
    for photo_to_remove in scripts_photos:
        file_path = os.path.join(f"static/images/scripts/{script_id}", photo_to_remove)
        os.remove(file_path)
    # Удаление текста
    os.remove(script.text_file_path)
    # Удаление оценок
    for mark in script.marks:
        delete_mark(mark.id)
    # Удаление комментариев
    for review in script.reviews:
        delete_review(review.id)
    # Удаление самого объекта
    db_sess.delete(script)
    db_sess.commit()


def edit_script_data(script_id, title, description, type, genres, photo_path, text_file):
    # Функция для редактирования сценария
    script = db_sess.get(Script, script_id)
    script.title = title
    script.description = description
    script.type = type
    script.genres = genres
    # Если приложены новое фото и текст, устанавливаем их
    if photo_path:
        set_photo_for_object(script, photo_path, TYPES_OF_SCRIPTS_PHOTOS_AND_SIZES)
    if text_file:
        set_script_file_for_script(script, text_file)
    db_sess.commit()


def get_script_by_id(script_id):
    script = db_sess.get(Script, script_id)
    return script


def get_user_scripts(user_id):
    return get_user_attribute_value(user_id, "scripts")


def get_all_scripts():
    all_scripts = db_sess.query(Script).all()
    return list(all_scripts)


# Функции для просмотров сценариев


def add_script_to_viewed_scripts(user_id, script_id):
    # Добавление сценария в просмотренные пользователем
    user = db_sess.get(User, user_id)
    script = db_sess.get(Script, script_id)
    if script not in user.viewed_scripts:
        user.viewed_scripts.append(script)
        script.views_count += 1
        db_sess.commit()


# Функции для подписок


def make_user_subscriber_of_another_user(user_id, target_id):
    # Функция для подписки одного пользователя на другого
    user = db_sess.get(User, user_id)
    target = db_sess.get(User, target_id)
    user.subscriptions.append(target)
    target.subscribers_count += 1
    db_sess.commit()


def unsubscribe_user_from_another_user(user_id, target_id):
    # Функция отписки одного пользователя от другого
    user = db_sess.get(User, user_id)
    target = db_sess.get(User, target_id)
    target.subscribers_count -= 1
    user.subscriptions.remove(target)
    db_sess.commit()


def check_if_user_is_subscriber_of_another_user(user_id, target_id):
    # Функция проверки, подписан ли один пользователь на другого
    user = db_sess.get(User, user_id)
    target = db_sess.get(User, target_id)
    return user in target.subscribers


def get_subscribers_of_user(user_id):
    return get_user_attribute_value(user_id, "subscribers")


def get_subscriptions_of_user(user_id):
    return get_user_attribute_value(user_id, "subscriptions")


# Функции для оценок


def update_script_and_author_rating(script):
    # Функция обновления рейтинга сценария и пользователя. Вызывается при добавлении и удалении оценок
    previous_rating = script.rating
    if previous_rating > 6:
        script.author.rating -= previous_rating
    if not script.marks_count:
        script.rating = 0
    else:
        script.rating = round(sum(map(lambda mark: mark.mark, script.marks)) / script.marks_count, 1)
        if script.rating > 6:
            script.author.rating += script.rating

    db_sess.commit()


def add_new_mark(user_id, script_id, mark):
    # Фунция добавления оценки
    user = db_sess.get(User, user_id)
    script = db_sess.get(Script, script_id)
    # Если пользователь уже оценивал этот сценарий, то заменяем предыдущую оценку новой
    already_given_mark = db_sess.query(ScriptMark).filter(ScriptMark.user == user, ScriptMark.script == script).first()
    if already_given_mark:
        delete_mark(already_given_mark.id)
    new_mark = ScriptMark(script=script,
                              user=user,
                              mark=mark)
    script.marks_count += 1
    db_sess.add(new_mark)
    # пересчитываем рейтинг сценария и автора
    update_script_and_author_rating(script)
    db_sess.commit()


def delete_mark(mark_id):
    mark = db_sess.get(ScriptMark, mark_id)
    script = mark.script
    script.marks_count -= 1
    db_sess.delete(mark)
    update_script_and_author_rating(script)
    db_sess.commit()


def get_all_scripts_marks(script_id):
    return get_script_attribute_value(script_id, "marks")


def get_all_users_given_script_marks(user_id):
    return get_user_attribute_value(user_id, "given_script_marks")


# Функции для рецензий


def add_new_review(user_id, script_id, title, text):
    # Добавление рецензии
    user = db_sess.get(User, user_id)
    script = db_sess.get(Script, script_id)
    # Если пользователь уже добавлял рецензию на этот сценарий, удаляем ее и заменяем новой
    already_given_review = db_sess.query(ScriptReview).filter(ScriptReview.user == user,
                                                              ScriptReview.script == script).first()
    if already_given_review:
        delete_review(already_given_review.id)
    new_review = ScriptReview(user=user,
                                  script=script,
                                  title=title,
                                  text=text)
    script.reviews_count += 1
    db_sess.add(new_review)
    db_sess.commit()


def delete_review(review_id):
    # Удаление рецензии
    review = db_sess.get(ScriptReview, review_id)
    db_sess.delete(review)
    db_sess.commit()


def get_all_scripts_reviews(script_id):
    return get_script_attribute_value(script_id, "reviews")


def get_all_users_given_script_reviews(user_id):
    return get_user_attribute_value(user_id, "given_script_reviews")


# Общие функции


def get_scripts_for_main_page(user_id, page_number, scripts_per_page=40):
    # Функция для получения сценариев для основной страницы сайта
    # Может вызываться как с user_id, так и без него (со значением None), в зависимости от того,
    # был ли произведен воход в аккаунт
    # Это нужно для того, чтобы сортировать сценарии на главной странице для каждого пользователя персонально -
    # чтобы сначала шли сценарии, которые он не смотрел, а также авторов, на которых он подписан и т.д.

    # Если пользователь указан, то получаем его из базы данных
    if user_id is not None:
        user = db_sess.get(User, user_id)

    result = sorted(db_sess.query(Script).all(),
                    # сортировка по свойствам сценариев
                    key=lambda script: (script not in user.viewed_scripts if user_id else True,
                                        script.date_of_publication,
                                        script.author in user.subscriptions if user_id else True,
                                        script.marks_count,
                                        script.rating,
                                        script.views_count),
                    reverse=True)[scripts_per_page * (page_number - 1): scripts_per_page * page_number]

    return result


def get_total_scripts_count():
    # Получение количества сценариев на сайте. Нужно, чтобы отображать пагинацию
    # на главной странице (в противном случае, будет неизвестно кол-во страниц)
    result = len(set(db_sess.query(Script)))
    return result


def get_main_page_pages_count(scripts_per_page=40):
    # Получение количества страниц на главной странице сайта
    scripts_count = get_total_scripts_count()
    return scripts_count // scripts_per_page + (
        1 if scripts_count % scripts_per_page or scripts_count == 0 else 0)


def get_users_best_scripts(user):
    # Получение лучших сценариев пользователя
    scripts = sorted(user.scripts, key=lambda script: (script.rating,
                                                       script.marks_count,
                                                       script.views_count,
                                                       script.date_of_publication), reverse=True)[:5]
    return scripts
