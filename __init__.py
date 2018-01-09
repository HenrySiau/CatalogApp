from flask import Flask
from CatalogApp.models import User

app = Flask(__name__)
app.config.from_object('config')
app.config.from_pyfile('instance_config.py')


@app.route("/")
def index():
    result = ''
    users = User.query.all()
    for user in users:
        result += str(user.name)
    return 'This is main page, users: ' + result


if __name__ == '__main__':
    app.run()
