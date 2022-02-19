import sqlite3

class DB:

    def __init__(self):
        # connect to database
        self.conn = sqlite3.connect('accounts.db')

        # create cursor
        self.c = self.conn.cursor()

        self.c.execute(""" CREATE TABLE IF NOT EXISTS accounts (
                    name text,
                    email text,
                    password text
        );""")
        self.conn.commit()

    def createUser(self, name, email, password):
        self.c.execute('INSERT INTO accounts VALUES (?, ?, ?)', [name, email, password])
        self.conn.commit()

    def getUser(self, email):
        self.c.execute('SELECT * FROM accounts WHERE email=?', [email])
        data = self.c.fetchall()
        if data:
            d = data[0]
            return {
                'name': d[0],
                'email': d[1],
                'password': d[2]
            }
        else:
            return None

    # datatype:
    # null - exist or not
    # integer
    # real
    # text
    # blob - mp3, image, stored as it is

    def close(self):
        self.conn.close()