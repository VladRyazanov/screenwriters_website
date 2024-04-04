from requests import get, delete

"""
Файл для тестирования api
"""

# Получение всех пользователей
print(get("http://localhost:5001/api/v2/users").json())
# Получение пользователя по id
print(get("http://localhost:5001/api/v2/users/1").json())
# Передача несуществующего id - {'message': 'user 1 not found'}
print(get("http://localhost:5001/api/v2/users/999").json())
# Удаление пользователя
print(delete("http://localhost:5001/api/v2/users/1").json())