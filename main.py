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
# ----------------------------------------------------------------------------------------------------------------------


# --------------обработка url-------------------------------------------------------------------------------------------

# ----------------приветствие-------------------------------------------------------------------------------------------
@app.route('/hello')
def hello():
    return render_template('index.html')


# ------------------Главная страница------------------------------------------------------------------------------------
@app.route('/')
@app.route('/main')
def main():
    tasks = Task.query.order_by(Task.date).all()  # получить все записи из БД отсортированные по полю date
    return render_template('main.html', tasks=tasks)


# ------------------------Форма создания задачи-------------------------------------------------------------------------
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


# ------------------------Форма редактирования задачи-------------------------------------------------------------------
@app.route('/tasks/<int:id>/update', methods=['POST', 'GET'])
def update(id):
    detail_task = Task.query.get(id)
    if request.method == "POST":

        # 1) Заполняем атрибуты объекта данными из формы

        detail_task.header = request.form['header']
        detail_task.intro = request.form['intro']
        detail_task.text = request.form['text']

        # 2) Обновление записи в базе данных

        try:
            db.session.commit()  # должно обновить запись в бд без всяких update O_o
            return redirect('/')
        except:
            return "Я что-то нажал и всё исчезло"  # Добавь обработку разных ошибок

    else:
        return render_template('task_update.html', detail_task=detail_task)


# ------------------------Форма детального отображения задачи-----------------------------------------------------------
@app.route('/tasks/<int:id>')
def tasks_detail(id):
    detail_task = Task.query.get(id)  # забрать из базы данных значение по конкретному id
    return render_template('task_detail.html', task=detail_task)


# ------------------------Форма удаления записи-------------------------------------------------------------------------
@app.route('/tasks/<int:id>/delete')
def tasks_delete(id):
    detail_task = Task.query.get_or_404(id)  # если записи нет, будет ошибка 404
    try:
        db.session.delete(detail_task)
        db.session.commit()
        return redirect('/')
    except:
        return "При удалении статьи произошла ошибка"  # добавить обработку разных ошибок и окно подтверждения удаления


# ---------------------рендер о нас-------------------------------------------------------------------------------------
@app.route('/about')
def about():
    return render_template('about.html')


# -----------------------Заготовка для авторизации----------------------------------------------------------------------
@app.route('/user/<string:username>/<int:id>')  # Обработка любых username и id
def user(username, id):
    return f"user page: {username}, id: {id}"


# -------------запуск приложения------------------------------------------------------
if __name__ == "__main__":
    app.run(debug=True)
    db.create_all()
