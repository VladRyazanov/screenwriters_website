from data import db_session
from data.script import Script
from data.script_mark import ScriptMark
from data.script_review import ScriptReview
from data.user import User


def init_database(database_path="db/data.db"):
    db_session.global_init(database_path)


# Декораторы и служебные функции


def error_checker(func):
    # Декоратор, который вызывает переданную функцию в блоке try-except,
    # при возникновении ошибки возвращает сообщение
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as error:
            return {"success": False, "message": f"Error: {error} (from decorator)"}

    return wrapper


@error_checker
def id_checker(class_of_object_to_check_id, id_keyword_argument_name, check_two_objects=False,
               second_id_keyword_argument_name=None):
    # Декоратор, который применяется к функциям, где требуется получение объекта по id,
    # например, при действиях с пользователями по id.
    # Данный декоратор проверяет, есть ли требуемый объект в базе данных.
    # Если пользователь не будет найден, то функция не будет вызвана
    # В качестве аргумента данный декоратор принимает класс объекта, который нужно искать в базе данных,
    # это может быть класс пользователя (User), сценария (Script), и т.д.
    # Из-за наличия этого аргумента пришлось поместить сам декоратор в функцию,
    # т.к. иначе передать в декоратор аргумент нельзя.
    def decorator(func):
        def wrapper(*args, **kwargs):
            db_sess = db_session.create_session()
            objects_ids = list()
            if id_keyword_argument_name in kwargs:
                objects_ids.append(kwargs[id_keyword_argument_name])
            else:
                objects_ids.append(args[0])
            if check_two_objects:
                if second_id_keyword_argument_name in kwargs:
                    objects_ids.append(kwargs[second_id_keyword_argument_name])
                else:
                    objects_ids.append(args[1])
            if all([db_sess.get(class_of_object_to_check_id, object_id) for object_id in objects_ids]):
                return func(*args, **kwargs)

            return {"success": False, "message": f"{class_of_object_to_check_id.__name__} not found (from decorator)"}

        return wrapper

    return decorator


@id_checker(User, "user_id")
@error_checker
def get_user_attribute_value(user_id, attribute_name):
    db_sess = db_session.create_session()
    user = db_sess.get(User, user_id)
    return {"success": True, "result": getattr(user, attribute_name)}


@id_checker(Script, "script_id")
@error_checker
def get_script_attribute_value(script_id, attribute_name):
    db_sess = db_session.create_session()
    script = db_sess.get(Script, script_id)
    return {"success": True, "result": getattr(script, attribute_name)}


# Функции для пользователей


@error_checker
def add_new_user(name, description, photo_path, email, password, social_networks=""):
    db_sess = db_session.create_session()
    if db_sess.query(User).filter(User.email == email).first():
        return {"success": False, "message": "User already exists"}

    new_user = User(name=name,
                    description=description,
                    photo_path=photo_path,
                    email=email,
                    social_networks=social_networks)
    new_user.set_password(password)
    db_sess.add(new_user)
    db_sess.commit()
    return {'success': True}


@id_checker(User, "user_id")
@error_checker
def delete_user(user_id):
    db_sess = db_session.create_session()
    user = db_sess.get(User, user_id)
    # получение всего, что связано с пользователем
    all_user_scripts = get_user_scripts(user_id)
    all_user_marks = get_all_users_given_script_marks(user_id)
    all_user_reviews = get_all_users_given_script_reviews(user_id)
    # проверка результатов получения
    for result in [all_user_scripts, all_user_marks, all_user_reviews]:
        if not result["success"]:
            return {"success": False, "message": result["message"]}
    results = list()
    # удаление сценариев
    for script in all_user_scripts["result"]:
        results.append(delete_script(script.id))
    # удаление оценок
    for mark in all_user_marks["result"]:
        results.append(delete_mark(mark.id))
    # удаление рецензий
    for review in all_user_reviews["result"]:
        results.append(delete_review(review.id))
    # проверка результатов удаления
    for result in results:
        if not result["success"]:
            return {"success": False, "message": result["message"]}
    # если все результаты положительны, удаляем самого пользователя и подтверждаем совершенные операции
    db_sess.delete(user)
    db_sess.commit()
    return {"success": True}


@id_checker(User, "user_id")
def get_user_by_id(user_id):
    db_sess = db_session.create_session()
    user = db_sess.get(User, user_id)
    return {"success": True, "result": user}


@error_checker
def get_all_users():
    db_sess = db_session.create_session()
    all_users = db_sess.query(User).all()
    return {"success": True, "users": [user for user in all_users]}


# Функции для сценариев


@id_checker(User, "author_user_id")
@error_checker
def add_new_script(author_user_id, title, description, photo_path, type, genres, text):
    db_sess = db_session.create_session()
    user = db_sess.get(User, author_user_id)
    new_script = Script(title=title,
                        description=description,
                        photo_path=photo_path,
                        type=type,
                        genres=genres,
                        text=text,
                        author=user)
    db_sess.add(new_script)
    db_sess.commit()
    return {'success': True}


@id_checker(Script, "script_id")
@error_checker
def delete_script(script_id):
    db_sess = db_session.create_session()
    script = db_sess.get(Script, script_id)
    db_sess.delete(script)
    db_sess.commit()
    return {"success": True}


@id_checker(Script, "script_id")
@error_checker
def get_script_by_id(script_id):
    db_sess = db_session.create_session()
    script = db_sess.get(Script, script_id)
    return {"success": True, "result": script}


def get_user_scripts(user_id):
    return get_user_attribute_value(user_id, "scripts")


@error_checker
def get_all_scripts():
    db_sess = db_session.create_session()
    all_scripts = db_sess.query(Script).all()
    return {"success": True, "result": [script for script in all_scripts]}


# Функции для просмотров сценариев


@id_checker(User, "user_id")
@id_checker(Script, "script_id")
@error_checker
def add_script_to_viewed_scripts(user_id, script_id):
    db_sess = db_session.create_session()
    user = db_sess.get(User, user_id)
    script = db_sess.get(Script, script_id)
    user.viewed_scripts.append(script)
    script.views_count += 1
    db_sess.commit()
    return {"success": True}


# Функции для подписок


@id_checker(User, "user_id", check_two_objects=True, second_id_keyword_argument_name="target_id")
@error_checker
def make_user_subscriber_of_another_user(user_id, target_id):
    db_sess = db_session.create_session()
    user = db_sess.get(User, user_id)
    target = db_sess.get(User, target_id)
    user.subscriptions.append(target)
    target.subscribers_count += 1
    db_sess.commit()
    return {'success': True}


@id_checker(User, "user_id", check_two_objects=True, second_id_keyword_argument_name="target_id")
@error_checker
def unsubscribe_user_from_another_user(user_id, target_id):
    db_sess = db_session.create_session()
    user = db_sess.get(User, user_id)
    target = db_sess.get(User, target_id)
    target.subscribers_count -= 1
    user.subscriptions.remove(target)
    db_sess.commit()
    return {'success': True}


@id_checker(User, "user_id", check_two_objects=True, second_id_keyword_argument_name="target_id")
@error_checker
def check_if_user_is_subscriber_of_another_user(user_id, target_id):
    db_sess = db_session.create_session()
    user = db_sess.get(User, user_id)
    target = db_sess.get(User, target_id)
    return {"success": True, "result": user in target.subscribers}


def get_subscribers_of_user(user_id):
    return get_user_attribute_value(user_id, "subscribers")


def get_subscriptions_of_user(user_id):
    return get_user_attribute_value(user_id, "subscriptions")


# Функции для оценок


@id_checker(User, "user_id")
@id_checker(Script, "script_id")
@error_checker
def add_new_mark(user_id, script_id, mark):
    db_sess = db_session.create_session()
    user = db_sess.get(User, user_id)
    script = db_sess.get(Script, script_id)

    already_given_mark = db_sess.query(ScriptMark).filter(ScriptMark.user == user, ScriptMark.script == script).first()
    if already_given_mark:
        already_given_mark.mark = mark
    else:
        new_mark = ScriptMark(script=script,
                              user=user,
                              mark=mark)
        script.marks_count += 1
        db_sess.add(new_mark)
    db_sess.commit()
    return {"success": True}


@id_checker(ScriptMark, "mark_id")
@error_checker
def delete_mark(mark_id):
    db_sess = db_session.create_session()
    mark = db_sess.get(ScriptMark, mark_id)
    mark.script.marks_count -= 1
    db_sess.delete(mark)
    db_sess.commit()
    return {"success": True}


def get_all_scripts_marks(script_id):
    return get_script_attribute_value(script_id, "marks")


def get_all_users_given_script_marks(user_id):
    return get_user_attribute_value(user_id, "given_script_marks")


# Функции для рецензий


@id_checker(User, "user_id")
@id_checker(Script, "script_id")
@error_checker
def add_new_review(user_id, script_id, text):
    db_sess = db_session.create_session()
    user = db_sess.get(User, user_id)
    script = db_sess.get(Script, script_id)

    already_given_review = db_sess.query(ScriptReview).filter(ScriptReview.user == user,
                                                              ScriptReview.script == script).first()
    if already_given_review:
        already_given_review.text = text
    else:
        new_review = ScriptReview(user=user,
                                  script=script,
                                  text=text)
        script.reviews_count += 1
        db_sess.add(new_review)
    db_sess.commit()
    return {"success": True}


@id_checker(ScriptReview, "review_id")
@error_checker
def delete_review(review_id):
    db_sess = db_session.create_session()
    review = db_sess.get(ScriptReview, review_id)
    review.script.reviews_count -= 1
    db_sess.delete(review)
    db_sess.commit()
    return {"success": True}


def get_all_scripts_reviews(script_id):
    return get_script_attribute_value(script_id, "reviews")


def get_all_users_given_script_reviews(user_id):
    return get_user_attribute_value(user_id, "given_script_reviews")


# Общие функции


@id_checker(User, "user_id")
@error_checker
def get_scripts_for_main_page(user_id, page_number, scripts_per_page=40):
    db_sess = db_session.create_session()
    user = db_sess.get(User, user_id)

    result = sorted(db_sess.query(Script).all(),
                    key=lambda script: (script not in user.viewed_scripts,
                                        script.author in user.subscriptions,
                                        script.marks_count,
                                        script.rating,
                                        script.views_count),
                    reverse=True)[scripts_per_page * (page_number - 1): scripts_per_page * page_number]

    return {"success": True, "result": result}
