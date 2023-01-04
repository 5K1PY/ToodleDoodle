# ToodleDoodle
ToodleDoodle is web tool for arranging meetings. Built on Flask, JQuery and PostgreSQL. 
 
## Installation
With running PostgreSQL database run:
```
./init_db.py
```
It will ask you database access info and then create required tables.

Alternatively create ``config.py`` file (as described in ``config.example.py``)
and then create tables in database by executing ``schema.sql`` in database.

## Running
To run the web server simply run in the main folder:
```
./flask run
```