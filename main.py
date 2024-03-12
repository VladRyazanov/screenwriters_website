from flask import Flask, render_template, url_for

app = Flask(__name__)


class Script:
    def __init__(self, title, genre, author, image_path, author_image_path):
        self.title = title
        self.genre = genre
        self.author = author
        self.image_path = image_path
        self.author_image_path = author_image_path



# Маршрут для главной страницы
@app.route('/')
def index():
    # Передаем пустой список сценариев для примера
    scripts = [Script("Первый сценарий", "Драма", "Влад Hzpfyjd",
                      url_for("static", filename="images/Снимок экрана 2024-03-08 в 11.39.15.png"),
                      url_for("static", filename="images/Снимок экрана 2024-03-08 в 12.30.27.png")) for i in range(10)]
    return render_template('index.html', scripts=scripts, total_pages_count=5, current_page_number=2)


if __name__ == '__main__':
    app.run()
