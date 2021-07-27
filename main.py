from flask import Flask


app = Flask(__name__)


@app.route('/')
def hello():
    return "hello"


@app.route('/main')
def main():
    return 'main page'


if __name__ == "__main__":
    app.run(debug=True)
