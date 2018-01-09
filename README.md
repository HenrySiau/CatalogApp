# Catalog App
Catalog App is an application that provides a list of items within a variety of categories as well as provide a user registration and authentication system. Registered users will have the ability to post, edit and delete their own items. 

## Installation
Python==3 or greater<br>
Flask==0.12.2<br>
SQLAlchemy==1.1.15 <br>
The Google APIs Client Library for Python:<br>
pip install --upgrade google-api-python-client<br>
pip install --upgrade google-auth google-auth-oauthlib google-auth-httplib2<br>
pip install --upgrade requests<br>

you can see my packages at requirements.txt<br>

## Set up the database
You can modify database setting at database.py<br>
to initiate database, run $ python init_db.py<br>

## Usage
Once installed the packages and set up your database, run $ python views.py to start flask server.<br>
you can then open main page at http://localhost:8000/ , inside the main page, click Register button to register a new user or click login button to login with google sign in.<br>
To fetch json data of a catalog, go to http://localhost:8000/api/catalog/catalog-name/items/json<br>
you can get item detail in json format by typing http://localhost:8000/api/item/item-slug/json<br>

after logged in, click your name at the header section to open console page, at console page, you will be able to create, edit, delete catalogs or items there, you can also go to console page by typing http://localhost:8000/my-console at your browser.
