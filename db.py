import psycopg2
import secrets
from config import HOST, DATABASE, USER, PASSWORD

from constants import AVAILABILITY
from poll import Poll

def db_operation(f):
    def g(*args, **kwargs):
        connection = psycopg2.connect(
                host=HOST,
                dbname=DATABASE,
                user=USER,
                password=PASSWORD
        )
        cur = connection.cursor()
        # cur.execute('PRAGMA foreign_keys = ON')

        value = f(cur, *args, **kwargs)

        connection.commit()
        cur.close()
        connection.close()
        return value
    return g


@db_operation
def init(connection):
    with open('schema.sql') as f:
        connection.execute(f.read())

@db_operation
def clear(connection):
    connection.execute("""
        DROP TABLE polls CASCADE;
        DROP TABLE poll_options CASCADE;
        DROP TABLE poll_data CASCADE;
    """)

@db_operation
def make_poll(connection, name, description, options):
    same_secrets = True
    while same_secrets:
        secret = secrets.token_urlsafe(16)
        connection.execute(
            'SELECT id FROM polls WHERE id=%s;',
            (secret,)
        )
        same_secrets = connection.fetchall()

    connection.execute(
        'INSERT INTO polls VALUES (%s, %s, %s, NULL);',
        (secret, name, description)
    )
    for option in options:
        connection.execute(
            """INSERT INTO poll_options(poll_id, poll_option)
            VALUES (%s, %s);""",
            (secret, option)
        )

    return secret


@db_operation
def poll_exists(connection, id):
    connection.execute(
        'SELECT id FROM polls WHERE id=%s;',
        (id,)
    )
    return len(connection.fetchall()) > 0


@db_operation
def read_poll(connection, poll_id):
    connection.execute(
        'SELECT title, description, closed FROM polls WHERE id=%s',
        (poll_id,)
    )
    name, description, closed = connection.fetchall()[0]
    connection.execute(
        'SELECT id, poll_option FROM poll_options WHERE poll_id=%s',
        (poll_id,)
    )
    options = connection.fetchall()
    connection.execute(
        """SELECT poll_data.username FROM poll_options
        JOIN poll_data ON poll_options.id=poll_data.poll_option_id
        WHERE poll_options.poll_id=%s
        GROUP BY poll_data.username
        ORDER BY poll_data.username;
        """,
        (poll_id,)
    )
    users = connection.fetchall()

    connection.execute(
        """SELECT poll_options.id, poll_data.username, poll_data.entry FROM poll_options
        JOIN poll_data ON poll_options.id=poll_data.poll_option_id
        WHERE poll_options.poll_id=%s;
        """,
        (poll_id,)
    )
    entries = connection.fetchall()
    return Poll(name, description, closed, options, users, entries)

@db_operation
def write_poll(connection, name, option_ids, choices):
    for option_id, choice in zip(option_ids, choices):
        connection.execute(
            """INSERT INTO poll_data(poll_option_id, username, entry)
            VALUES (%s, %s, %s)""",
            (option_id, name, AVAILABILITY.index(choice))
        )

@db_operation
def user_filled_poll(connection, poll_id, user):
    connection.execute(
        """SELECT * FROM poll_data
        INNER JOIN poll_options ON poll_data.poll_option_id=poll_options.id
        WHERE poll_options.poll_id=%s AND poll_data.username=%s""",
        (poll_id, user),
    )
    return len(connection.fetchall()) > 0

@db_operation
def delete_user_from_poll(connection, poll_id, user):
    connection.execute(
        """DELETE FROM poll_data
        WHERE id IN (
            SELECT poll_data.id FROM poll_data
            INNER JOIN poll_options ON poll_data.poll_option_id=poll_options.id
            WHERE poll_options.poll_id=%s AND poll_data.username=%s
        )""",
        (poll_id, user),
    )

@db_operation
def edit_poll_db(connection, poll_id, description, new_options):
    connection.execute(
        "UPDATE polls SET description=%s WHERE id=%s",
        (description, poll_id)
    )
    connection.execute(
        """SELECT poll_option FROM poll_options WHERE poll_id=%s
        ORDER BY poll_option""",
        (poll_id,)
    )
    options = connection.fetchall()
    options = list(map(lambda x: x[0], options))
    new_options.sort()

    i, j = 0, 0
    while (i < len(options) or j < len(new_options)):
        if i < len(options) and (j == len(new_options) or options[i] < new_options[j]):
            connection.execute(
                "DELETE FROM poll_options WHERE poll_id=%s AND poll_option=%s",
                (poll_id, options[i])
            )
            i += 1
        elif i == len(options) or options[i] > new_options[j]:
            connection.execute(
                "INSERT INTO poll_options(poll_id, poll_option) VALUES (%s, %s);",
                (poll_id, new_options[j])
            )
            j += 1
        else:
            i += 1
            j += 1


@db_operation
def close_poll_db(connection, poll_id, final_option):
    connection.execute(
        'SELECT id FROM poll_options WHERE poll_id=%s AND poll_option=%s',
        (poll_id, final_option)
    )
    final_option_id = connection.fetchall()[0][0]
    
    connection.execute(
        'UPDATE polls SET closed=%s WHERE id=%s',
        (final_option_id, poll_id,)
    )

@db_operation
def reopen_poll(connection, poll_id):
    connection.execute(
        'UPDATE polls SET closed=NULL WHERE id=%s',
        (poll_id,)
    )

if __name__ == "__main__":
    # don't run this accidentally
    # clear()
    # init()
    pass
