from asyncio.windows_events import NULL
import sqlite3

class DB:

    def __init__(self):
        # connect to database
        self.conn = sqlite3.connect('accounts.db')

        # create cursor
        self.c = self.conn.cursor()

        self.c.execute(""" CREATE TABLE IF NOT EXISTS accounts (
                    name text,
                    username text PRIMARY KEY,
                    password text
        );""")
        self.conn.commit()

    def createUser(self, name, username, password):
        self.c.execute('INSERT INTO accounts VALUES (?, ?, ?)', [name, username, password])

        self.c.execute(""" CREATE TABLE IF NOT EXISTS {}Books (
                    title text,
                    author text,
                    startDate text,
                    endDate text,
                    rating integer,
                    genres text,
                    cover blob,
                    review text
        );""".format(username))

        self.conn.commit()

    def getUser(self, username):
        self.c.execute('SELECT * FROM accounts WHERE username=?'.format(username), [username])
        data = self.c.fetchall()
        if data:
            d = data[0]
            return {
                'name': d[0],
                'username': d[1],
                'password': d[2]
            }
        else:
            return None

    def addBook(self, username, title, author, startDate, endDate, rating, genres, cover, review):
        self.c.execute('INSERT INTO {}books VALUES (?, ?, ?, ?, ?, ?, ?, ?)'.format(username), [title, author, startDate, endDate, rating, genres, cover, review])
        self.conn.commit()

    def getBook(self, title, username):
        self.c.execute('SELECT * FROM {}books WHERE title=?'.format(username), [title])
        data = self.c.fetchall()
        if data:
            d = data[0]
            return {
                'title': d[0],
                'author': d[1],
                'startDate': d[2],
                'endDate': d[3],
                'rating': d[4],
                'genres': d[5],
                'cover': d[6],
                'review': d[7]
            }
        else:
            return None

    def getAllBooks(self, username):
        data = self.c.execute('SELECT * FROM {}books ORDER BY endDate'.format(username))
        return [{
            'title': d[0],
            # 'author': d[1],
            # 'startDate': d[2],
            # 'endDate': d[3],
            # 'rating': d[4],
            # 'genres': d[5],
            'cover': d[6],
            # 'review': d[7]
        } for d in data]

    
    def deleteBook(self, name):
        self.c.execute('DELETE FROM books WHERE name=?', [name])
    # datatype:
    # null - exist or not
    # integer
    # real
    # text
    # blob - mp3, image, stored as it is

    def close(self):
        self.conn.close()

# class books:
#     def __init__(self, username):
#         # connect to database
#         self.conn = sqlite3.connect(username + "Books.db")

#         # create cursor
#         self.c = self.conn.cursor()

#         self.c.execute(""" CREATE TABLE IF NOT EXISTS books (
#                     title text,
#                     author text,
#                     startDate text,
#                     endDate text,
#                     rating integer,
#                     genres text,
#                     cover blob,
#                     review text
#         );""")
#         self.conn.commit()

    
#     def close(self):
#         self.conn.close()
