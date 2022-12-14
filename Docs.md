## Overview
Whole project consists of several files. Main groups of them are:
 - `.py` files - Run the server-side part.
 - `templates` - Folder of html files for pages.
 - `static/js` - Folder of JavaScript files for their respective pages.

## Build
Only file for build is `setup_app.py`.
It builds the project for running.

## Backend
Files for backend and their purpose:
 - `main.py` - handling http request and communicating with all other modules
 - `form.py` - handling polls submitted by the user
 - `poll.py` - internal representation of poll results
 - `db.py` - working with the database
 - `schema.sql` - database schema
 - `constants.py` - file with program constants
 - `config.py` - stores secret token and database access data

## Frontend
Frontend files and what they are used for (`html` files are in `templates/` and `js`
in `static/js`):
 - `base.html` and `base.js` - Files used by all pages (non-changing code such as top bar or nojs warning)
 - `settings.js` - handles settings hotkeys
 and synchronizes them with cookies
 - `index.html` - Welcome page
 - `new_poll.html` and `new_poll.js` - Page for creating poll
 - `poll.html` and `poll.js` - Poll page
 - `poll_formats.html` - Various poll formats for poll page
 - `edit_poll.html` and `edit_poll.js` - Page for editing poll
 - `closed_poll` - Page of a closed poll 

## User - server communication
User communicates with server by one of two ways:
 - query part of url (for simple operation or preparing to do an operation):
    - preparing to edit an entry
    - deleting a poll entry
    - preparing to edit poll
    - reopening poll
 - html forms:
    - creating / editing a table
    - filling / editing in a poll entry
    - closing poll

Additionally preferred active modes of the poll (such as transposed table or interval mode) are stored in cookies.

## Database
The project uses PostgreSQL database. In the
database are stored following tables:
 - `polls` - table of all polls
 - `poll_options` - stores options for each poll
 - `poll_data` - stores filled-in availability of
 users in particular poll

## Libraries
The project uses following nonstandard python libraries:
 - [Flask](https://flask.palletsprojects.com/) for running the server 
 - [WTForms](https://wtforms.readthedocs.io/) for easier handling of forms
 - [Flask-WTF](https://flask-wtf.readthedocs.io/) for integration between Flask and WTForms
 in flask
 - [psycopg2-binary] for PostgeSQL database
