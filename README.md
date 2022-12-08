# ToodleDoodle
ToodleDoodle is web tool for arranging meeting. Built on Flask, JQuery and PostgreSQL. 

## Instalation
The project uses following nonstandard python libaries:
 - [Flask](https://flask.palletsprojects.com/) for running the server 
 - [WTForms](https://wtforms.readthedocs.io/) for easier handling of forms
 - [Flask-WTF](https://flask-wtf.readthedocs.io/) for integration between Flask and WTForms
 in flask
 - [psycopg2-binary] for PostgeSQL database

Next for installing all requirements simply run:
```
./setup
```
It will install required packages and ask You about access info for PostgreSQL database.


## Running
To run the web server simply run in the main folder:
```
./flask run
```