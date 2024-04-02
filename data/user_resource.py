from flask import jsonify
from flask_restful import abort, Resource

from data.data_services import *


def abort_if_user_not_found(user_id):
    user = get_user_by_id(user_id)
    if not user:
        abort(404, message=f"user {user_id} not found")


class UserResource(Resource):
    def get(self, users_id):
        abort_if_user_not_found(users_id)
        return jsonify({'user': get_user_by_id(users_id).to_dict(only=["name", "description", "email", "social_networks",
                                                                      "rating", "modified_date"])})

    def delete(self, users_id):
        abort_if_user_not_found(users_id)
        delete_user(users_id)
        return jsonify({'success': 'OK'})


class UserListResource(Resource):
    def get(self):
        users = get_all_users()  # Получаем всех пользователей
        user_dicts = [user.to_dict(only=["name", "description", "email",
                                         "social_networks", "rating", "modified_date"]) for user in users]  # Преобразуем каждого пользователя в словарь
        return jsonify({'users': user_dicts})
