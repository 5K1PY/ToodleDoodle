import psycopg2
import secrets
from config import HOST, DATABASE, USER, PASSWORD

from constants import AVAILABILITY
from poll import Poll

def db_operation(f):
    def g(self, *args, **kwargs):
        value = f(self, *args, **kwargs)

        self.connection.commit()
        return value
    return g

class DB:
    def __init__(self):
        self.connection = psycopg2.connect(
                host=HOST,
                dbname=DATABASE,
                user=USER,
                password=PASSWORD
        )
        self.cur = self.connection.cursor()
    
    def close(self):
        self.cur.close()
        self.connection.close()

    @db_operation
    def init(self):
        with open('schema.sql') as f:
            self.cur.execute(f.read())

    @db_operation
    def clear(self):
        self.cur.execute("""
            DROP TABLE polls CASCADE;
            DROP TABLE poll_options CASCADE;
            DROP TABLE poll_data CASCADE;
        """)

    @db_operation
    def make_poll(self, name, description, options):
        same_secrets = True
        while same_secrets:
            secret = secrets.token_urlsafe(16)
            self.cur.execute(
                'SELECT id FROM polls WHERE id=%s;',
                (secret,)
            )
            same_secrets = self.cur.fetchall()

        self.cur.execute(
            'INSERT INTO polls VALUES (%s, %s, %s, NULL);',
            (secret, name, description)
        )
        for option in options:
            self.cur.execute(
                """INSERT INTO poll_options(poll_id, poll_option)
                VALUES (%s, %s);""",
                (secret, option)
            )

        return secret


    @db_operation
    def poll_exists(self, id):
        self.cur.execute(
            'SELECT id FROM polls WHERE id=%s;',
            (id,)
        )
        return len(self.cur.fetchall()) > 0


    @db_operation
    def read_poll(self, poll_id):
        self.cur.execute(
            'SELECT title, description, closed FROM polls WHERE id=%s',
            (poll_id,)
        )
        name, description, closed = self.cur.fetchall()[0]
        self.cur.execute(
            'SELECT id, poll_option FROM poll_options WHERE poll_id=%s',
            (poll_id,)
        )
        options = self.cur.fetchall()
        self.cur.execute(
            """SELECT poll_data.username FROM poll_options
            JOIN poll_data ON poll_options.id=poll_data.poll_option_id
            WHERE poll_options.poll_id=%s
            GROUP BY poll_data.username
            ORDER BY poll_data.username;
            """,
            (poll_id,)
        )
        users = self.cur.fetchall()

        self.cur.execute(
            """SELECT poll_options.id, poll_data.username, poll_data.entry FROM poll_options
            JOIN poll_data ON poll_options.id=poll_data.poll_option_id
            WHERE poll_options.poll_id=%s;
            """,
            (poll_id,)
        )
        entries = self.cur.fetchall()
        return Poll(name, description, closed, options, users, entries)

    @db_operation
    def write_poll(self, name, option_ids, choices):
        for option_id, choice in zip(option_ids, choices):
            self.cur.execute(
                """INSERT INTO poll_data(poll_option_id, username, entry)
                VALUES (%s, %s, %s)""",
                (option_id, name, AVAILABILITY.index(choice))
            )

    @db_operation
    def user_filled_poll(self, poll_id, user):
        self.cur.execute(
            """SELECT * FROM poll_data
            INNER JOIN poll_options ON poll_data.poll_option_id=poll_options.id
            WHERE poll_options.poll_id=%s AND poll_data.username=%s""",
            (poll_id, user),
        )
        return len(self.cur.fetchall()) > 0

    @db_operation
    def delete_user_from_poll(self, poll_id, user):
        self.cur.execute(
            """DELETE FROM poll_data
            WHERE id IN (
                SELECT poll_data.id FROM poll_data
                INNER JOIN poll_options ON poll_data.poll_option_id=poll_options.id
                WHERE poll_options.poll_id=%s AND poll_data.username=%s
            )""",
            (poll_id, user),
        )

    @db_operation
    def edit_poll_db(self, poll_id, description, new_options):
        self.cur.execute(
            "UPDATE polls SET description=%s WHERE id=%s",
            (description, poll_id)
        )
        self.cur.execute(
            """SELECT poll_option FROM poll_options WHERE poll_id=%s
            ORDER BY poll_option""",
            (poll_id,)
        )
        options = self.cur.fetchall()
        options = list(map(lambda x: x[0], options))
        new_options.sort()

        i, j = 0, 0
        while (i < len(options) or j < len(new_options)):
            if i < len(options) and (j == len(new_options) or options[i] < new_options[j]):
                self.cur.execute(
                    "DELETE FROM poll_options WHERE poll_id=%s AND poll_option=%s",
                    (poll_id, options[i])
                )
                i += 1
            elif i == len(options) or options[i] > new_options[j]:
                self.cur.execute(
                    "INSERT INTO poll_options(poll_id, poll_option) VALUES (%s, %s);",
                    (poll_id, new_options[j])
                )
                j += 1
            else:
                i += 1
                j += 1


    @db_operation
    def close_poll_db(self, poll_id, final_option):
        self.cur.execute(
            'SELECT id FROM poll_options WHERE poll_id=%s AND poll_option=%s',
            (poll_id, final_option)
        )
        final_option_id = self.cur.fetchall()[0][0]
        
        self.cur.execute(
            'UPDATE polls SET closed=%s WHERE id=%s',
            (final_option_id, poll_id,)
        )

    @db_operation
    def reopen_poll(self, poll_id):
        self.cur.execute(
            'UPDATE polls SET closed=NULL WHERE id=%s',
            (poll_id,)
        )

if __name__ == "__main__":
    # don't run this accidentally
    db = DB()
    # db.clear()
    # db.init()
    pass
