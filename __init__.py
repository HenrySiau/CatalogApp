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

@app.route('/<catalog_name>/items')
def catalog_detail(catalog_name):
    """List items under a specific catalog"""
    catalog = Catalog.query.filter(Catalog.name == catalog_name).first()
    if len(catalog.items) == 0:
        flash('There are no item in this catalog')
        return redirect(url_for('index'))
    return render_template('catalog_detail.html', catalog=catalog)


@app.route('/catalog/new', methods=['GET', 'POST'])
@login_required
@csrf_token_required
def new_catalog():
    """Create a new catalog"""
    if request.method == 'POST':
        name = clean_data(request.form['name'])
        if Catalog.query.filter(Catalog.name == name).first():
            flash('Catalog name already exist, please choose another one')
            return redirect(url_for('new_catalog'))
        user_id = session.get('user_id')
        new_catalog = Catalog(name=name, user_id=user_id)
        db_session.add(new_catalog)
        try:
            db_session.commit()
        except:
            flash('Something went wrong, please try again')
            return redirect(url_for('new_catalog'))

        flash("new catalog {} had successfully added".format(name))
        print("new catalog {} had successfully added".format(name))
        return redirect(url_for('console'))
    else:
        catalogs = Catalog.query.all()
        return render_template('new_catalog.html', catalogs=catalogs)


@app.route('/catalog/<catalog_name>/edit', methods=['GET', 'POST'])
@login_required
@csrf_token_required
def edit_catalog(catalog_name):
    """Edit Catalog"""
    catalog = Catalog.query.filter(Catalog.name == catalog_name).first()
    # Validate the catalog belongs to current user
    if not catalog.user_id == session.get('user_id'):
        flash("you can't edit other user's catalog")
        print("user id:{} trying to edit other user's catalog".format(
            str(session.get('user_id'))))
        return redirect(url_for('console'))

    if request.method == 'POST':
        new_catalog_name = clean_data(request.form['name'])
        # validate catalog name is unit
        if not validate_catalog_name(new_catalog_name):
            flash('{} already exist, please select another name'.format(new_catalog_name))
            return render_template('edit_catalog.html', catalog_name=catalog_name)
        else:
            old_catalog_name = catalog.name
            catalog.name = new_catalog_name
            db_session.add(catalog)
            try:
                db_session.commit()
            except:
                flash('something went wrong, please try again')
                return render_template('edit_catalog.html',
                                       catalog_name=catalog_name)
            flash(
                "Catalog name '{}' had been successfully changed to '{}'".format(
                    old_catalog_name, new_catalog_name))
            print(
                "Catalog name '{}' had been successfully changed to '{}'".format(
                    old_catalog_name, new_catalog_name))
            return redirect(url_for('console'))
    else:
        return render_template('edit_catalog.html', catalog_name=catalog_name)


@app.route('/catalog/<catalog_name>/delete', methods=['GET', 'POST'])
@login_required
@csrf_token_required
def delete_catalog(catalog_name):
    """Delete a selected catalog"""
    catalog = Catalog.query.filter(Catalog.name == catalog_name).first()
    # validate the catalog belongs to current user
    if not catalog.user_id == session.get('user_id'):
        flash("you can't delete other user's catalog")
        print("user id:{} trying to delete other user's catalog".format(
            str(session.get('user_id'))))
        return redirect(url_for('console'))

    if request.method == 'POST':
        # in case someone get around with default GET method
        if len(catalog.items) > 0:
            flash('Can not delete catalog with item in it')
            return redirect('/{}/items'.format(catalog.name))
        try:
            db_session.delete(catalog)
            db_session.commit()
        except:
            flash('Something went wrong, can not delete this catalog')
            return redirect(url_for('console'))
        flash("catalog '{}' had been deleted".format(catalog_name))
        print("catalog '{}' had been deleted".format(catalog_name))
        return redirect(url_for('console'))
    else:
        num_items = len(catalog.items)
        return render_template('delete_catalog.html', catalog_name=catalog_name, num_items=num_items)


@app.route('/item/<slug>')
def get_item(slug):
    """Show detail of a selected item"""
    item = Item.query.filter(Item.slug == slug).first()
    return render_template('item_detail.html', item=item)


@app.route('/item/new', methods=['GET', 'POST'])
@login_required
@csrf_token_required
def new_item():
    """Create a new Item"""
    if request.method == 'POST':
        slug = clean_data(request.form['slug']).replace(' ', '-')
        if not validate_item_slug(slug):
            flash('this slug already exist, please choose other one')
            return redirect(url_for('new_item'))
        name = clean_data(request.form['name'])
        description = clean_data(request.form['description'])
        catalog_id = clean_data(request.form['catalog_id'])
        user_id = session.get('user_id')

        new_item = Item(name=name,
                        description=description,
                        catalog_id=catalog_id,
                        slug=slug,
                        user_id=user_id)
        db_session.add(new_item)
        try:
            db_session.commit()
        except:
            flash('Something went wrong, please try again')
            return redirect(url_for('new_item'))
        flash("New item '{}' had been successfully created".format(name))
        print("New item '{}' had been successfully created".format(name))
        return redirect(url_for('console'))
    else:
        catalogs = Catalog.query.all()
        return render_template('new_item.html', catalogs=catalogs)


@app.route('/item/<slug>/edit', methods=['GET', 'POST'])
@login_required
@csrf_token_required
def edit_item(slug):
    catalogs = Catalog.query.all()
    item = Item.query.filter(Item.slug == slug).first()
    # validate the item belongs to current user
    if not item.user_id == session.get('user_id'):
        flash("you can't edit other user's item")
        print("user id:{} trying to edit other user's item".format(
            str(session.get('user_id'))))
        return redirect(url_for('console'))
    if request.method == 'POST':
        new_slug = clean_data(request.form['slug'])
        new_name = clean_data(request.form['name'])
        new_catalog_id = int(clean_data(request.form['catalog_id']))
        new_description = clean_data(request.form['description'])
        user_id = session.get('user_id')
        if new_slug == slug:
            item.name = new_name
            item.description = new_description
            item.catalog_id = new_catalog_id
            item.user_id = user_id
            db_session.add(item)
            try:
                db_session.commit()
            except:
                flash('something went wrong, please try again')
                return render_template('edit_item.html',
                                       item=item, catalogs=catalogs)
            return redirect(url_for('console'))
        # validate new slug
        elif not validate_item_slug(new_slug):
            flash('URL slug already exist, please choose other one')
            return render_template('edit_item.html',
                                   item=item, catalogs=catalogs)
        else:
            item.name = new_name
            item.slug = new_slug
            item.description = new_description
            item.catalog_id = new_catalog_id
            item.user_id = user_id
            db_session.add(item)
            try:
                db_session.commit()
            except:
                flash('something went wrong, please try again')
                return render_template('edit_item.html',
                                       item=item, catalogs=catalogs)
            flash("Item '{}' had been modified".format(new_name))
            print("Item '{}' had been modified".format(new_name))
            return redirect(url_for('console'))

    else:
        return render_template('edit_item.html', item=item, catalogs=catalogs)


@app.route('/item/<slug>/delete', methods=['GET', 'POST'])
@login_required
@csrf_token_required
def delete_item(slug):
    """Delete an selected item"""
    item = Item.query.filter(Item.slug == slug).first()
    if not item.user_id == session.get('user_id'):
        flash("you can't delete other user's item")
        print("user id:{} trying to delete other user's item".format(
            str(session.get('user_id'))))
        return redirect(url_for('console'))
    if request.method == 'POST':
        try:
            db_session.delete(item)
            db_session.commit()
        except:
            flash('something went wrong, please try again')
            return render_template('delete_item.html', item_name=item.name)

        flash('Item "{}" had been successfully deleted'.format(item.name))
        print('Item "{}" had been successfully deleted'.format(item.name))
        return redirect(url_for('console'))
    else:
        return render_template('delete_item.html', item_name=item.name)


@app.route('/my-console')
@login_required
def console():
    """This function render a page that shows catalogs and items created by current user,
     and also show links to edit or delete catalogs or items.
    """
    user_id = session.get('user_id')
    print(user_id)
    catalogs = Catalog.query.filter(Catalog.user_id == user_id).all()
    items = Item.query.filter(Item.user_id == user_id).order_by(desc(Item.created_date)).all()
    return render_template('console.html', catalogs=catalogs, items=items)


@app.route('/login', methods=['GET', 'POST'])
@csrf_token_required
def login():
    """this function implement a conventional login
    """
    if request.method == 'POST':
        email = clean_data(request.form['email'])
        hashed_psd = hash_password(clean_data(request.form['password']))
        user = User.query.filter(User.email == email).first()
        if not user:
            flash('User email does not exist')
            return redirect(url_for('login'))
        # prevent social auth client login with empty password
        if not user.password_setup:
            flash('Your password have not setup yet')
            return redirect(url_for('register'))
        if not user.password == hashed_psd:
            flash('Password incorrect')
            return redirect(url_for('login'))
        else:
            session['user_name'] = user.name
            session['user_email'] = user.email
            session['user_id'] = user.id
            print('user id:{} had just logged in'.format(str(user.id)))
            return redirect(url_for('index'))
    else:
        # pass current_app to the page so it can access google client id from config
        app_ = current_app
        return render_template('login.html', app=app_)


@app.route('/logout')
def logout():
    """log out user
    """
    del session['user_name']
    del session['user_email']
    del session['user_id']
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
@csrf_token_required
def new_user():
    """create a new user from register page(not social authentication)"""
    if request.method == 'POST':
        user_name = clean_data(request.form['user_name'])
        email = clean_data(request.form['email'])
        print(email)
        if not request.form['password'] == request.form['cnf_password']:
            flash('passwords does not match')
            return redirect(url_for('new_user'))
        password = clean_data(request.form['password'])
        if not validate_user_email(email):
            flash('Email already exist, please choose other one or login')
            return redirect(url_for('new_user'))
        if not validate_user_password(password):
            flash('password length must be 6 digit/character or more')
            return redirect(url_for('new_user'))
        else:
            hashed_psd = hash_password(password)
            user = User(name=user_name, email=email, password=hashed_psd, password_setup=True)
            db_session.add(user)
            try:
                db_session.commit()
            except:
                flash('Something went wrong, please try again.')
                return redirect(url_for('new_user'))
            flash('new user had been created')
            return redirect(url_for('login'))
    else:
        return render_template('register.html')


@app.route('/tokensignin', methods=['GET', 'POST'])
def token_login():
    """google sign in, validate client token and fetch client information from google
    """
    if request.method == 'POST':
        if session.get('user_id'):
            flash('You had already login')
            print('You had already login')
            return 'You had already login'
        token = request.form['idtoken']
        client_id = current_app.config['GOOGLE_CLIENT_ID']
        try:
            idinfo = id_token.verify_oauth2_token(
                token, google_auth_request.Request(), client_id)

            if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
                raise ValueError('Wrong issuer.')
            user_name = idinfo['name']
            user_email = idinfo['email']
            user = User.query.filter(User.email == user_email).first()
            if not user:
                print('create a new user')
                user = User(name=user_name, email=user_email, password_setup=False, password=None)
                db_session.add(user)
                try:
                    db_session.commit()
                except:
                    flash('Can not login with this user')
                    print('Can not create this user')
                    return 'Can not add this user to our system'
            session['user_name'] = user_name
            session['user_email'] = user_email
            session['user_id'] = User.query.filter(User.email == user_email).first().id

        except ValueError:
            # Invalid token
            flash('Invalid token')
            print('Invalid token')
            return redirect(url_for('login'))
        print('success')
        return 'success'
    else:
        return redirect(url_for('login'))


if __name__ == '__main__':
    app.run()
