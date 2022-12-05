# ToodleDoodle
ToodleDoodle is web tool for arranging meeting. Built on Flask and JQuery. 

## Instalation
The project uses following nonstandard python libaries:
 - [Flask](https://flask.palletsprojects.com/) for running the server 
 - [WTForms](https://wtforms.readthedocs.io/) for easier handling of forms
 - [Flask-WTF](https://flask-wtf.readthedocs.io/) for integration between Flask and WTForms

For installing all of them simply run:
```
pip install Flask Flask-WTF WTForms
```

Then run 
```
python setup.py
```
to create `secret_config.py` file.


TODO: Running flask