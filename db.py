import sqlite3
import secrets
from constants import AVAILABILTY

from poll import Poll

def db_operation(f):
    def g(*args, **kwargs):
        connection = sqlite3.connect('database.db')

        value = f(connection, *args, **kwargs)

        connection.commit()
        connection.close()
        return value
    return g


@db_operation
def init(connection):
    with open('schema.sql') as f:
        connection.executescript(f.read())


@db_operation
def make_poll(connection, name, options):
    same_secrets = True
    while same_secrets:
        secret = secrets.token_urlsafe(16)
        same_secrets = connection.execute(
            'SELECT id FROM polls WHERE id=?;',
            (secret,)
        ).fetchall()

    connection.execute(
        'INSERT INTO polls VALUES (?, ?);',
        (secret, name)
    )
    for option in options:
        connection.execute(
            """INSERT INTO poll_options(poll_id, option)
            VALUES (?, ?);""",
            (secret, option)
        )

    return secret


@db_operation
def poll_exists(connection, id):
    return len(connection.execute(
        'SELECT id FROM polls WHERE id=?;',
        (id,)
    ).fetchall()) > 0


@db_operation
def read_poll(connection, id):
    name = connection.execute(
        'SELECT title FROM polls WHERE id=?',
        (id,)
    ).fetchall()[0][0]

    options = connection.execute(
        'SELECT id, option FROM poll_options WHERE poll_id=?',
        (id,)
    ).fetchall()

    users = connection.execute(
        """SELECT poll_data.user FROM poll_options
        JOIN poll_data ON poll_options.id==poll_data.poll_option_id
        WHERE poll_options.poll_id=?
        GROUP BY poll_data.user
        ORDER BY poll_data.user;
        """,
        (id,)
    ).fetchall()

    entries = (connection.execute(
        """SELECT poll_options.id, poll_data.user, poll_data.entry FROM poll_options
        JOIN poll_data ON poll_options.id==poll_data.poll_option_id
        WHERE poll_options.poll_id=?;
        """,
        (id,)
    ).fetchall())

    return Poll(name, options, users, entries)

@db_operation
def write_poll(connection, name, option_ids, choices):
    for option_id, choice in zip(option_ids, choices):
        connection.execute(
            """INSERT INTO poll_data(poll_option_id, user, entry)
            VALUES (?, ?, ?)""",
            (option_id, name, AVAILABILTY.index(choice))
        )

if __name__ == "__main__":
    # don't run this accidentally
    # init()
    pass