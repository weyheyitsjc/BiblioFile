from flask import Flask, render_template, g, request, redirect, session, jsonify
from database import DB
import os

app = Flask(__name__, static_folder='public', static_url_path='')
secret_key = os.urandom(32)
app.config['SECRET_KEY'] = secret_key

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = DB()
    return db

# def bookDB(username):
#     booksDB = getattr(g, '_database', None)
#     if booksDB is None:
#         booksDB = books(username)
#     return booksDB

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
    message = None
    if request.method == 'POST':
        name = request.form['name']
        username = request.form['username']
        password = request.form['password']
        if (get_db().getUser(username) == None):
            if name and username and password:
                get_db().createUser(name, username, password)
                return redirect('/')
        else:
            message = "Username already exists. Please choose another one."
    return render_template('/signup.html', message = message)

@app.route('/login', methods=['GET', 'POST'])
def login():
    message = None
    if request.method == 'POST':
        username = request.form['username']
        typed_password = request.form['password']
        if username and typed_password:
            user = get_db().getUser(username)
            if user:
                if (typed_password == user['password']):
                    session['user'] = user
                    return redirect('/')
                else:
                    message = "Username and password do not match, please try again."
            else:
                message = "Username and password do not match, please try again."
        elif username and not typed_password:
            message = "Missing password, please try again."
        elif not username and typed_password:
            message = "Missing username, please try again."
    return render_template('index.html', message=message)

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
            if i == genres[0]: 
                stringGenres += i
            else:
                stringGenres += ", " + i

        if title and author and endDate and rating and genres:
            get_db().addBook(session['user']['username'], title, author, startDate, endDate, rating, stringGenres, cover, review)
        return redirect('/')
    return render_template('/addbook.html')

@app.route('/api/mybooks')
def api_mybooks():
    if 'user' in session:
        response = get_db().getAllBooks(session['user']['username'])
        return jsonify(response)
    else:
        return jsonify('Error: User not authenticated')

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/')

if __name__ == "__main__":
    app.run(debug=True)