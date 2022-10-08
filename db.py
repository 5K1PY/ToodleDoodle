import sqlite3
import secrets

def db_operation(f):
    def g(*args, **kwargs):
        connection = sqlite3.connect('database.db')

        f(connection, *args, **kwargs)

        connection.commit()
        connection.close()
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
            f'SELECT id FROM polls WHERE id="{secret}";'
        ).fetchall()

    connection.execute(
        f'INSERT INTO polls VALUES ("{secret}", "{name}");'
    )
    for option in options:
        connection.execute(
            f"""INSERT INTO poll_options(poll_id, option)
            VALUES ("{secret}", "{option}");"""
        )


@db_operation
def read_poll(connection, id):
    pass


if __name__ == "__main__":
    # don't run this accidentally
    init()
    pass
    make_poll("Test", ["1", "2", "3"])