from flask import Flask
from models import User

app = Flask(__name__)
app.config.from_pyfile('config.py')
app.config.from_pyfile('instance_config.py')


@app.route("/")
def index():
    result = ''
    users = User.query.all()
    for user in users:
        result += str(user.name)
    return 'This is main page, users: ' + result

@app.route("/hello")
def hello():
    return 'hello'


if __name__ == '__main__':
    app.run()
