from flask import Flask, render_template, url_for


app = Flask(__name__)


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


if __name__ == "__main__":
    app.run(debug=True)
