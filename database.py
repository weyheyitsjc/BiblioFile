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
                    cover text,
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
        self.c.execute('SELECT rowid, * FROM {}books WHERE title=?'.format(username), [title])
        data = self.c.fetchall()
        if data:
            d = data[0]
            return {
                'id':d[0],
                'title': d[1],
                'author': d[2],
                'startDate': d[3],
                'endDate': d[4],
                'rating': d[5],
                'genres': d[6],
                'cover': d[7],
                'review': d[8]
            }
        else:
            return None

    def getAllBooks(self, username):
        data = self.c.execute('SELECT * FROM {}books ORDER BY endDate'.format(username))
        return [{
            'title': d[0],
            'cover': d[6],
        } for d in data]

    def deleteBook(self, title, username):
        self.c.execute('DELETE FROM {}books WHERE title=?'.format(username), [title])
        self.conn.commit()

    def updateTitle(self, id, title, username):
        self.c.execute('UPDATE {}books SET title=? WHERE id=?'.format(username), [title, id])
        self.conn.commit()

    def updateAuthor(self, id, author, username):
        self.c.execute('UPDATE {}books SET author=? WHERE id=?'.format(username), [author, id])
        self.conn.commit()

    def updateStartDate(self, id, startDate, username):
        self.c.execute('UPDATE {}books SET startDate=? WHERE id=?'.format(username), [startDate, id])
        self.conn.commit()

    def updateEndDate(self, id, endDate, username):
        self.c.execute('UPDATE {}books SET endDate=? WHERE id=?'.format(username), [endDate, id])
        self.conn.commit()

    def updateRating(self, id, rating, username):
        self.c.execute('UPDATE {}books SET rating=? WHERE id=?'.format(username), [rating, id])
        self.conn.commit()

    def updateGenres(self, id, genres, username):
        self.c.execute('UPDATE {}books SET genres=? WHERE id=?'.format(username), [genres, id])
        self.conn.commit()

    def updateCover(self, id, cover, username):
        self.c.execute('UPDATE {}books SET cover=? WHERE id=?'.format(username), [cover, id])
        self.conn.commit()

    def updateReview(self, id, review, username):
        self.c.execute('UPDATE {}books SET review=? WHERE id=?'.format(username), [review, id])
        self.conn.commit()

    def close(self):
        self.conn.close()