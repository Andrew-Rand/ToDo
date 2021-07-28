from flask import Flask, render_template, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:1111@localhost/tod'  # выбор базы данных
db = SQLAlchemy(app)


# -----------------создание объекта для базы данных-------------------------------------
class Task(db.Model):  # внутри класса прописываются поля таблицы
    id = db.Column(db.Integer, primary_key=True)  # уникальный идентификатор для каждой задачи (обязательно!)
    header = db.Column(db.String(100), nullable=False)  # заголовок
    intro = db.Column(db.String(300), nullable=False)  # краткое описание
    text = db.Column(db.Text, nullable=False)  # описание
    date = db.Column(db.DateTime, default=datetime.utcnow)  # дата и время (по умолчанию "сейчас")

    def __repr__(self):
        return "<Article %r>" % self.id
# --------------------------------------------------------------------------------------


# --------------обработка url------------------------------------------------------------
@app.route('/hello')
def hello():
    return render_template('index.html')


@app.route('/')
@app.route('/main')
def main():
    return render_template('main.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/user/<string:username>/<int:id>')  # Обработка любых username и id
def user(username, id):
    return f"user page: {username}, id: {id}"


# -------------запуск приложения------------------------------------------------------
if __name__ == "__main__":
    app.run(debug=True)
    db.create_all()
