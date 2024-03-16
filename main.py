from flask import Flask, render_template, url_for
from data.services import *


app = Flask(__name__)

init_database()

# просто для теста
print(add_new_user("Влад", "", "static/images/Снимок экрана 2024-03-08 в 12.30.27.png", "email", "123"))
for _ in range(5):
    for i in range(1, 10):
        print(add_new_script(1, f"Сценарий {i}", "Описание", f"static/images/{i}.png", "фильм", "драма, триллер", "текст"))

@app.route('/<>')
def index():
    return scripts_page()
@app.route('/scripts/<int:user_id>/<int:page_number>')
def scripts_page(user_id, page_number):
    scripts = get_scripts_for_main_page(user_id, page_number)["result"]
    return render_template('index.html', scripts=scripts, total_pages_count=100, current_page_number=page_number)

if __name__ == '__main__':
    app.run()
