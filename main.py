from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:1111@localhost/todo'  # выбор базы данных
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://{user}:{password}@{server}/{database}'.format(user='root', password='1111', server='localhost', database='todo')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # отключить ворнинг
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
    tasks = Task.query.order_by(Task.date).all()  # получить все записи из БД отсортированные по полю date
    return render_template('main.html', tasks=tasks)


@app.route('/create', methods=['POST', 'GET'])  # url может отрабатывать в post (когда отправлка формы) либо прямой заход
def create():
    if request.method == "POST":

        # 1) Заполняем переменные данными из формы

        header = request.form['header']
        intro = request.form['intro']
        text = request.form['text']

        # 2) Передаём данные в объект базы данных

        task = Task(header=header, intro=intro, text=text)

        # 3) Сохраняем объект в базу данных
        try:
            db.session.add(task)
            db.session.commit()
            return redirect('/')
        except:
            return "Задача не добавлена из-за критической ошибки"  # Добавь обработку разных ошибок

    else:
        return render_template('create.html')


@app.route('/tasks/<int:id>')
def tasks_detail(id):
    detail_task = Task.query.get(id)
    return render_template('task_detail.html', task=detail_task)


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
