# # # # # scripts_count = 81
# # # # # scripts_per_page = 40
# # # # # print({"success": True, "result": scripts_count // scripts_per_page + (1 if scripts_count % scripts_per_page else 0)})
# # # # #
# # # # #
# # # import time
# # #
# # from data.data_services import *
# #
# #
# print(", ".join(["1"]))
# # init_database()
# # # print("Добавляю пользователя 1", add_new_user(name="Влад",
# # #              description="Второй пользователь",
# # #              photo_path="static/images/temporary_photos/2023-11-08_14.53.30.png",
# # #              email="email2",
# # #              password="234"))
# # # print("Добавление сценария для пользователя 1",
# # #                 add_new_script(1, f"Название 1", "description", f"static/images/1.png", "film", "drama", "text"))
# # print([i.big_photo_path for i in get_all_scripts()["result"]])
# #
# # # print(delete_script(2))
# # # print(append_to_best_scripts_table(get_all_scripts()["result"][0]))
# # # print(get_best_scripts_top("during_the_day"))
# # # print(add_script_to_best_scripts_top("during_the_day", get_script_by_id(1)["result"]))
# # # print(get_best_scripts_top("during_the_day"))
# # # #
# # # init_database("db/data.db")
# # # # print(get_scripts_for_main_page(None, 1))
# # #
# # #
# # # # # from sqlalchemy import create_engine, MetaData, Table, Column, Integer
# # # # # from sqlalchemy.orm import sessionmaker
# # # # #
# # # # # # # Подключение к базе данных
# # # # # # db_url = 'sqlite:///your_database.db'  # Подставьте вашу базу данных
# # # # # # engine = create_engine(db_url)
# # # # # #
# # # # # # # Определение объекта MetaData
# # # # # # metadata = MetaData()
# # # # # #
# # # # # # # Определение таблицы site_general_data
# # # # # # site_general_data = Table('site_general_data', metadata,
# # # # # #     Column("total_users_count", Integer, default=0),
# # # # # #     Column('total_scripts_count', Integer, default=0)
# # # # # # )
# # # # # #
# # # # # # # Создание сеанса
# # # # # # Session = sessionmaker(bind=engine)
# # # # # # session = Session()
# # # # # #
# # # # # # # Функция для обновления значения общего количества пользователей
# # # # # # def update_total_users_count():
# # # # # #     try:
# # # # # #         # Увеличиваем значение общего количества пользователей на 1
# # # # # #         session.execute(site_general_data.update().values(total_users_count=site_general_data.c.total_users_count + 1))
# # # # # #         session.commit()
# # # # # #     finally:
# # # # # #         session.close()
# # # # # #
# # # # # # # Пример использования
# # # # # # if __name__ == '__main__':
# # # # # #     # Обновляем значение общего количества пользователей
# # # # # #     update_total_users_count()
# # # # #
# # # # # # from data import db_session
# # # # # # from data.site_general_data import site_general_data
# # # # # #
# # # # # # db_session.global_init("db/data.db")
# # # # # # db_sess = db_session.create_session()
# # # # # # result = db_sess.query(site_general_data.c.total_users_count).first()
# # # # # # print(result)
# # # # from data.services import *
# # # # # #
# # # # init_database()
# # # # print(get_user_by_id(1))
# # # # #
# # # # # #
# # # directory_for_photos_path = f"static/images/users/1"
# # # print(directory_for_photos_path.lstrip("static"))
# # # print("Добавляю пользователя 1", add_new_user(name="Влад",
# # #              description="Первый пользователь",
# # #              photo_path="Пока нет",
# # #              email="emaisdfghl",
# # #              password="234"))
# # # # # print(get_total_users_count())
# # # for _ in range(5):
# # #     for i in range(1, 10):
# # #         print("Добавление сценария для пользователя 1",
# # #                 add_new_script(1, f"Название {i}", "description", f"/images/{i}.png", "film", "drama", "text"))
# # #
# # # # # delete_script(3)
# # # # #
# # # # # print(get_total_scripts_count())
# # # # # # # print(check_if_user_is_subscriber_of_another_user(2, 3))
# #
# # # # # # # print("Все пользователи", get_all_users())
# # # # # #
# # # # # # # print("удаляю пользователя", delete_user(1))
# # # # # # # print("Подписчики пользователя 2", get_subscribers_of_user(2))
# # # # # # # print("Подписки пользователя 1", get_subscriptions_of_user(1))
# # # # # #
# # # # # # # print("Все пользователи", get_all_users())
# # # # # # # print("Подписываю пользователя 2 на пользователя 1", make_user_subscriber_of_another_user(2, 1))
# # # # # # # print("Подписчики пользователя 1", get_subscribers_of_user(1))
# # # # # # # print("Подписки пользователя 2", get_subscriptions_of_user(2))
# # # # # # # print()
# # # # # # # # user = get_user_by_id(1)["user"]
# # # # # # # print()
# # # # # # # print("Все сценарии", get_all_scripts())
# # # # # # for i in range(1, 10):
# # # # # #
# # # # # # print("Все сценарии", get_all_scripts())
# # # # # # print()
# # # # # #
# # # # # # print("Добавление сценария 1 в просмотренные у пользователя 2", add_script_to_viewed_scripts(2, 1))
# # # # # #
# # # # # # print("Просмотренные сценарии", get_user_by_id(2)["result"].viewed_scripts)
# # # # # # print()
# # # # # # print("Добавление оценки на  сценарий 3", add_new_mark(1, 3, 5))
# # # # # # print()
# # # # # # print("Получение всех сценариев для второго пользователя")
# # # # # # result = get_scripts_for_main_page(2, 1)
# # # # # # print(result)
# # # # # # print([f"{i.title} Оценок - {i.marks_count}" for i in result["result"]])
# # # # # # # print(get_all_scripts())
# # # # # #
# # # # # # # print(get_all_scripts_marks(1))
# # # # # # # print(get_all_users_marks(2))
# # # # # #
# # # # # #
# # # # # #
# # # # # #
# # # # # # # print("Добавление комментария", add_new_review(user_id=2, script_id=1, text="Плохой фильм"))
# # # # # # # print("Комментарии у сценария", get_all_scripts_reviews(1))
# # # # # # # print("Комментарии пользователя", get_all_users_given_script_reviews(2))
# # # # # # # print("Удаление пользователя", delete_user(user_id=2))
# # # # # # # print("Комментарии у сценария", get_all_scripts_reviews(1))
# # # # # # # print("Комментарии пользователя", get_all_users_given_script_reviews(2))
# # # # # # # # print(get_all_users())
# # # # # # # # print(delete_user(1))
# # # # # # # # print(get_all_users())
# # # # # # # print(get_all_scripts())
# # # # # # # print(get_user_scripts(1))
# # # # # # # # import json
# # # # # # # # print(delete_user(user_id=1))
# # # # # # # # print(get_all_users())
# # # # # # # # print(get_all_scripts())
# # # # # # # # from data.user import User
# # # # # # # # from data.db_session import create_session, global_init
# # # # # # # #
# # # # # # # # global_init("db/data.db")
# # # # # # # # db_sess = create_session()
# # # # # # # #
# # # # # # # # user1 = db_sess.query(User).filter(User.id == 1).first()
# # # # # # # # user2 = db_sess.query(User).filter(User.id == 2).first()
# # # # # # # # # user1.subscriptions.append(user2)
# # # # # # # # # db_sess.commit()
# # # # # # # # sb = {"subscribers": db_sess.query(User).filter(User.id == 2).first().subscribers}
# # # # # # # # print(sb)
# # #
# # # a = 1
# # # b = None
# # # print(a not in b if b else True)
import datetime

print(datetime.datetime.now().date())