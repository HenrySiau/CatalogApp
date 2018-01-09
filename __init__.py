from flask import Flask, current_app, session, request, redirect, render_template, url_for, flash
from models import User
from api import api_
from database import db_session
from models import User, Catalog, Item
from utility import login_required, clean_data, validate_user_email, csrf_token_required
from utility import validate_user_password, validate_catalog_name, validate_item_slug
from utility import hash_password
from sqlalchemy import desc
from google.oauth2 import id_token
from google.auth.transport import requests as google_auth_request

app = Flask(__name__)
app.config.from_pyfile('config.py')
app.config.from_pyfile('instance_config.py')
app.register_blueprint(api_, url_prefix='/api')


@app.teardown_appcontext
def shutdown_session(exception=None):
    """Disconnect database
    """
    db_session.remove()


@app.route("/")
def index():
    """Main page"""
    catalogs = Catalog.query.all()
    items = Item.query.order_by(desc(Item.created_date)).all()
    return render_template('index.html', catalogs=catalogs, items=items)

@app.route("/hello")
def hello():
    return 'hello'


if __name__ == '__main__':
    app.run()
