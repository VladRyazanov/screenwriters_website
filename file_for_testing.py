from data.services import *
#
init_database()
print("Добавляю пользователя 1", add_new_user(name="Влад",
             description="Первый пользователь",
             photo_path="Пока нет",
             email="email",
             password="234"))
# print(check_if_user_is_subscriber_of_another_user(2, 3))
print("Добавляю пользователя 2", add_new_user(name="Влад",
             description="Второй пользователь",
             photo_path="Пока нет",
             email="email2",
             password="234"))
# print("Все пользователи", get_all_users())

# print("удаляю пользователя", delete_user(1))
# print("Подписчики пользователя 2", get_subscribers_of_user(2))
# print("Подписки пользователя 1", get_subscriptions_of_user(1))

# print("Все пользователи", get_all_users())
# print("Подписываю пользователя 2 на пользователя 1", make_user_subscriber_of_another_user(2, 1))
# print("Подписчики пользователя 1", get_subscribers_of_user(1))
# print("Подписки пользователя 2", get_subscriptions_of_user(2))
# print()
# # user = get_user_by_id(1)["user"]
# print()
# print("Все сценарии", get_all_scripts())
for i in range(1, 10):
    print("Добавление сценария для пользователя 1",
          add_new_script(1, f"Название {i}", "description", "none", "film", "drama", "text"))
print("Все сценарии", get_all_scripts())
print()

print("Добавление сценария 1 в просмотренные у пользователя 2", add_script_to_viewed_scripts(2, 1))

print("Просмотренные сценарии", get_user_by_id(2)["result"].viewed_scripts)
print()
print("Добавление оценки на  сценарий 3", add_new_mark(1, 3, 5))
print()
print("Получение всех сценариев для второго пользователя")
result = get_scripts_for_main_page(2, 1)
print(result)
print([f"{i.title} Оценок - {i.marks_count}" for i in result["result"]])
# print(get_all_scripts())

# print(get_all_scripts_marks(1))
# print(get_all_users_marks(2))




# print("Добавление комментария", add_new_review(user_id=2, script_id=1, text="Плохой фильм"))
# print("Комментарии у сценария", get_all_scripts_reviews(1))
# print("Комментарии пользователя", get_all_users_given_script_reviews(2))
# print("Удаление пользователя", delete_user(user_id=2))
# print("Комментарии у сценария", get_all_scripts_reviews(1))
# print("Комментарии пользователя", get_all_users_given_script_reviews(2))
# # print(get_all_users())
# # print(delete_user(1))
# # print(get_all_users())
# print(get_all_scripts())
# print(get_user_scripts(1))
# # import json
# # print(delete_user(user_id=1))
# # print(get_all_users())
# # print(get_all_scripts())
# # from data.user import User
# # from data.db_session import create_session, global_init
# #
# # global_init("db/data.db")
# # db_sess = create_session()
# #
# # user1 = db_sess.query(User).filter(User.id == 1).first()
# # user2 = db_sess.query(User).filter(User.id == 2).first()
# # # user1.subscriptions.append(user2)
# # # db_sess.commit()
# # sb = {"subscribers": db_sess.query(User).filter(User.id == 2).first().subscribers}
# # print(sb)
