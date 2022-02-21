from flask import Flask, render_template, g, request, redirect, session
from database import DB, books
import os

app = Flask(__name__, static_folder='public', static_url_path='')
secret_key = os.urandom(32)
app.config['SECRET_KEY'] = secret_key

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = DB()
    return db

def bookDB(name):
    booksDB = getattr(g, '_database', None)
    if booksDB is None:
        booksDB = books(name)
    return booksDB

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        if name and email and password:
            get_db().createUser(name, email, password)
            bookDB(name)
            return redirect('/')
    return render_template('/signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    message = None
    if request.method == 'POST':
        email = request.form['email']
        typed_password = request.form['password']
        if email and typed_password:
            user = get_db().getUser(email)
            if user:
                if (typed_password == user['password']):
                    session['user'] = user
                    return redirect('/')
                else:
                    message = "Email and password do not match, please try again"
            else:
                message = "Email and password do not match, please try again"
        elif email and not typed_password:
            message = "Missing password, please try again"
        elif not email and typed_password:
            message = "Missing email, please try again"
    return render_template('login.html', message=message)

@app.route('/addbook', methods=['GET', 'POST'])
def addbook():
    if (session['user'] != None) and (request.method == 'POST'):
        title = request.form['title']
        author = request.form['author']
        startDate = request.form['startDate']
        endDate = request.form['endDate']
        rating = request.form.get('rating')
        genres = request.form.getlist('genres')
        cover = request.form['cover']
        review = request.form['review']

        stringGenres = ""
        for i in genres:
            stringGenres += i + " "

        if title and author and endDate and rating and genres:
            bookDB(session['user']['name']).addBook(title, author, startDate, endDate, rating, stringGenres, cover, review)
        return redirect('/')
    return render_template('/addbook.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/')

if __name__ == "__main__":
    app.run(debug=True)