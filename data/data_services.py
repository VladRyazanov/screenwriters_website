from data import db_session
from data.image_services import *
from data.script import Script
from data.script_mark import ScriptMark
from data.script_review import ScriptReview
from data.site_general_data import site_general_data
from data.script_text_services import *
from data.user import User

db_sess = None


def init_database(database_path="db/data.db"):
    global db_sess
    db_session.global_init(database_path)
    db_sess = db_session.create_session()
    db_sess.execute(site_general_data.insert().values({"total_users_count": 0,
                                                       "total_scripts_count": 0}))
    db_sess.commit()


def get_user_attribute_value(user_id, attribute_name):
    user = db_sess.get(User, user_id)
    return list(getattr(user, attribute_name))


def get_script_attribute_value(script_id, attribute_name):
    script = db_sess.get(Script, script_id)
    return getattr(script, attribute_name)


# Функции для пользователей


#
def add_new_user(name, description, photo_path, email, password, social_networks=""):
    new_user = User(name=name,
                    description=description,
                    email=email,
                    social_networks=social_networks)

    new_user.set_password(password)

    db_sess.execute(site_general_data.update().values({"total_users_count": site_general_data.c.total_users_count + 1}))
    db_sess.add(new_user)
    db_sess.commit()
    set_photo_for_object(new_user, photo_path, TYPES_OF_USERS_PHOTOS_AND_SIZES)
    db_sess.commit()

    return get_user_by_id(new_user.id)


def check_if_user_with_this_email_already_exists(email):
    if db_sess.query(User).filter(User.email == email).first():
        return True
    return False


def edit_user_data(user_id, name, description, photo):
    user = db_sess.get(User, user_id)
    user.name = name
    user.description = description
    if photo:
        set_photo_for_object(user, photo, TYPES_OF_USERS_PHOTOS_AND_SIZES)
    db_sess.commit()


def check_user_data_for_logging_in(email, password):
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

    os.remove(f"static/images/users/{user.id}")
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
    db_sess.execute(site_general_data.update().values(total_users_count=site_general_data.c.total_users_count - 1))
    db_sess.commit()


def get_user_by_id(user_id):
    user = db_sess.get(User, user_id)
    return user


def get_all_users():
    all_users = db_sess.query(User).all()
    return list(all_users)


# Функции для сценариев

def add_new_script(author_user_id, title, description, photo_path, type, genres, text_file):
    user = db_sess.get(User, author_user_id)
    new_script = Script(title=title,
                        description=description,
                        type=type,
                        genres=genres,
                        text_file_path="",
                        text="",
                        author=user)
    db_sess.add(new_script)

    db_sess.execute(site_general_data.update().values(total_scripts_count=site_general_data.c.total_scripts_count + 1))

    db_sess.commit()
    set_script_file_for_script(new_script, text_file)
    set_photo_for_object(new_script, photo_path, TYPES_OF_SCRIPTS_PHOTOS_AND_SIZES)
    db_sess.commit()


def delete_script(script_id):
    script = db_sess.get(Script, script_id)
    scripts_photos = os.listdir(f"static/images/scripts/{script_id}")
    for photo_to_remove in scripts_photos:
        file_path = os.path.join(f"static/images/scripts/{script_id}", photo_to_remove)
        os.remove(file_path)
    os.remove(script.text_file_path)
    for mark in script.marks:
        delete_mark(mark.id)
    for review in script.reviews:
        delete_review(review.id)
    db_sess.delete(script)
    db_sess.execute(site_general_data.update().values(total_scripts_count=site_general_data.c.total_scripts_count - 1))
    db_sess.commit()


def edit_script_data(script_id, title, description, type, genres, photo_path, text_file):
    script = db_sess.get(Script, script_id)
    script.title = title
    script.description = description
    script.type = type
    script.genres = genres
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
    user = db_sess.get(User, user_id)
    script = db_sess.get(Script, script_id)
    user.viewed_scripts.append(script)
    script.views_count += 1
    db_sess.commit()


# Функции для подписок


def make_user_subscriber_of_another_user(user_id, target_id):
    user = db_sess.get(User, user_id)
    target = db_sess.get(User, target_id)
    user.subscriptions.append(target)
    target.subscribers_count += 1
    db_sess.commit()



def unsubscribe_user_from_another_user(user_id, target_id):
    user = db_sess.get(User, user_id)
    target = db_sess.get(User, target_id)
    target.subscribers_count -= 1
    user.subscriptions.remove(target)
    db_sess.commit()


def check_if_user_is_subscriber_of_another_user(user_id, target_id):
    user = db_sess.get(User, user_id)
    target = db_sess.get(User, target_id)
    return user in target.subscribers


def get_subscribers_of_user(user_id):
    return get_user_attribute_value(user_id, "subscribers")


def get_subscriptions_of_user(user_id):
    return get_user_attribute_value(user_id, "subscriptions")


# Функции для оценок


def add_new_mark(user_id, script_id, mark):
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
    previous_rating = script.rating
    script.rating = round(sum(map(lambda mark: mark.mark, script.marks)) / script.marks_count, 1)
    if previous_rating > 6:
        script.author.rating -= previous_rating
    if script.rating > 6:
        script.author.rating += script.rating
    db_sess.commit()



def delete_mark(mark_id):
    mark = db_sess.get(ScriptMark, mark_id)
    db_sess.delete(mark)
    db_sess.commit()



def get_all_scripts_marks(script_id):
    return get_script_attribute_value(script_id, "marks")


def get_all_users_given_script_marks(user_id):
    return get_user_attribute_value(user_id, "given_script_marks")


# Функции для рецензий


def add_new_review(user_id, script_id, title, text):
    user = db_sess.get(User, user_id)
    script = db_sess.get(Script, script_id)

    already_given_review = db_sess.query(ScriptReview).filter(ScriptReview.user == user,
                                                              ScriptReview.script == script).first()
    if already_given_review:
        already_given_review.title = title
        already_given_review.text = text
    else:
        new_review = ScriptReview(user=user,
                                  script=script,
                                  title=title,
                                  text=text)
        script.reviews_count += 1
        db_sess.add(new_review)
    db_sess.commit()



def delete_review(review_id):
    review = db_sess.get(ScriptReview, review_id)
    db_sess.delete(review)
    db_sess.commit()



def get_all_scripts_reviews(script_id):
    return get_script_attribute_value(script_id, "reviews")


def get_all_users_given_script_reviews(user_id):
    return get_user_attribute_value(user_id, "given_script_reviews")


# Общие функции


def get_scripts_for_main_page(user_id, page_number, scripts_per_page=40):
    if user_id is not None:
        user = db_sess.get(User, user_id)
        if not user:
            return

    result = sorted(db_sess.query(Script).all(),
                    key=lambda script: (script not in user.viewed_scripts if user_id else True,
                                        script.date_of_publication,
                                        script.author in user.subscriptions if user_id else True,
                                        script.marks_count,
                                        script.rating,
                                        script.views_count),
                    reverse=True)[scripts_per_page * (page_number - 1): scripts_per_page * page_number]

    return result


def get_total_users_count():
    result = db_sess.query(site_general_data.c.total_users_count).first()[0]
    return result


def get_total_scripts_count():
    result = db_sess.query(site_general_data.c.total_scripts_count).first()[0]
    return result


def get_main_page_pages_count(scripts_per_page=40):
    scripts_count = get_total_scripts_count()
    return scripts_count // scripts_per_page + (
                1 if scripts_count % scripts_per_page or scripts_count == 0 else 0)


def get_users_best_scripts(user):
    scripts = sorted(user.scripts, key=lambda script: (script.rating,
                                                       script.marks_count,
                                                       script.views_count,
                                                       script.date_of_publication), reverse=True)[:5]
    return scripts
