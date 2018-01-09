"""
this module contain utility tools for other module
"""
from functools import wraps
from flask import redirect, current_app, session, request, flash, url_for
import hashlib
from models import User, Catalog, Item
import random


def login_required(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if not session.get('user_name'):
            flash("Please login first, redirecting to login page")
            return redirect('/login')
        else:
            return func(*args, **kwargs)

    return decorated_function


def get_config(arg):
    """fetch data from config file"""
    data = str(current_app.config[arg])
    return data


def clean_data(data):
    """We should never trust data sent from clients, here we have not implement filters
    to clean data yet
    """
    return data.strip()


def hash_password(password):
    """this is just a conventional way to hash password, not for production
    """
    hashed_psd = hashlib.sha224(password.encode()).hexdigest()
    return hashed_psd


def csrf_token_required(func):
    """prevent csrf attack by generate and verify token
    each time we receive a form from client side"""
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if request.method == 'POST':
            if not session['csrf_token'] == request.form['csrf_token']:
                flash('invalid CSRF Token')
                return redirect(url_for('index'))
            else:
                return func(*args, **kwargs)
        else:
            session['csrf_token'] = str(random.getrandbits(64))
            return func(*args, **kwargs)

    return decorated_function


def validate_user_email(email):
    """Verify if the email is already exist
    """
    if User.query.filter(User.email == email).first():
        return False
    else:
        return True


def validate_user_password(password):
    """need to implement other functions to validate password"""
    if len(password) < 6:
        return False
    else:
        return True


def validate_catalog_name(name):
    """we can implement more functions to validate catalog name
    such as sensitive words or length of the name
    here we just check if the catalog exist in database"""
    if Catalog.query.filter(Catalog.name == name).first():
        return False
    else:
        return True


def validate_item_slug(slug):
    """verify the url slug is unit"""
    if Item.query.filter(Item.slug == slug).first():
        return False
    else:
        return True


