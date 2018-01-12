# Catalog App
Catalog App is an application that provides a list of items within a variety of categories as well as provide a user registration and authentication system. Registered users will have the ability to post, edit and delete their own items. 

## Installation
Python==3 or greater<br>
$ pip install -r requirements.txt<br>

## Set up the database
in this app I use PostgreSQL, with user grader<br>
You can modify database setting at database.py if you use different database or different user name<br>
to initiate database, run $ python init_db.py<br>

## Usage
Once installed the packages and set up your database, run $ python views.py to start flask server.<br>
you can then open main page at http://localhost:8000/ , inside the main page, click Register button to register a new user or click login button to login with google sign in.<br>
To fetch json data of a catalog, go to http://localhost:8000/api/catalog/catalog-name/items/json<br>
you can get item detail in json format by typing http://localhost:8000/api/item/item-slug/json<br>

after logged in, click your name at the header section to open console page, at console page, you will be able to create, edit, delete catalogs or items there, you can also go to console page by typing http://localhost:8000/my-console at your browser.

## Deployment
This App is deployed at Amazon Lightsail on Ubuntu 16.04<br>
Web server: Apache2
ip address: 13.59.217.2<br>
URL: skynet.run<br>
The web server responds on port 80<br>
At the server side, I created a new user and given dudo access, also allow the new user to ssh the server with modified port.<br>
The fire wall had set to only allow SSH, HTTP and NTP.
