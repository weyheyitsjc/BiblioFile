from flask import Flask, render_template, g, request, redirect, session, jsonify
from database import DB
import os
from werkzeug.utils import secure_filename
import json

app = Flask(__name__, static_folder='public', static_url_path='')
secret_key = os.urandom(32)
app.config['SECRET_KEY'] = secret_key
app.config['UPLOAD_FOLDER'] = './public/pics/userBooks'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = DB()
    return db

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
        else:
            message = "Missing username and password, please try again."
    return render_template('index.html', message = message)

@app.route('/addbook', methods=['GET', 'POST'])
def addbook():
    if (session['user'] != None) and (request.method == 'POST'):
        title = request.form['title']
        author = request.form['author']
        startDate = request.form['startDate']
        endDate = request.form['endDate']
        rating = request.form.get('rating')
        genres = request.form.getlist('genres')
        cover = request.files.get('cover')
        review = request.form['review']

        stringGenres = ""
        for i in genres:
            if i == genres[0]: 
                stringGenres += i
            else:
                stringGenres += ", " + i

        coverPath = ""
        if cover:
            image = request.files.get('cover')
            filename = secure_filename(image.filename)
            path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            coverPath = "/pics/userBooks/" + filename
            image.save(path)
        else:
            coverPath = "/pics/blankbook.jpg"

        if title and author and endDate and rating and genres:
            get_db().addBook(session['user']['username'], title, author, startDate, endDate, rating, stringGenres, coverPath, review)
        return redirect('/mybooks')
    return render_template('/addbook.html')

@app.route('/api/mybooks')
def api_mybooks():
    if 'user' in session:
        response = get_db().getAllBooks(session['user']['username'])
        return jsonify(response)
    else:
        return jsonify('Error: User not authenticated')

@app.route('/mybooks')
def mybooks():
    if 'user' in session:
        return render_template('/mybooks.html')
    else:
        return jsonify('Error: User not authenticated')

@app.route('/displaybook', methods=['GET'])
def displaybook():
    if 'user' in session:
        title = request.args.get('title')
        response = get_db().getBook(title, session['user']['username'])
        return render_template('/displaybook.html', response=response)
    else:
        return jsonify('Error: User not authenticated')

@app.route('/editbook', methods=['GET', 'POST'])
def editbook():
    if 'user' in session and request.method=="GET":
        title = request.args.get('title')
        response = get_db().getBook(title, session['user']['username'])
        return render_template('/editbook.html', response=response)
    elif 'user' in session and request.method=="POST":
        id = request.form['id']
        title = request.form['title']
        get_db().updateTitle(id, title, session['user']['username'])

        author = request.form['author']
        get_db().updateAuthor(id, author, session['user']['username'])

        startDate = request.form['startDate']
        get_db().updateStartDate(id, startDate, session['user']['username'])

        endDate = request.form['endDate']
        get_db().updateEndDate(id, endDate, session['user']['username'])

        rating = request.form.get('rating')
        if (rating != ""):
            get_db().updateRating(id, rating, session['user']['username'])

        genres = request.form.getlist('genres')
        if (genres != ""):
            stringGenres = ""
            for i in genres:
                if i == genres[0]: 
                    stringGenres += i
                else:
                    stringGenres += ", " + i
            get_db().updateGenres(id, stringGenres, session['user']['username'])

        cover = request.files.get('cover')
        coverPath = ""
        if cover:
            image = request.files.get('cover')
            filename = secure_filename(image.filename)
            path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            coverPath = "/pics/userBooks/" + filename
            image.save(path)
            get_db().updateCover(id, coverPath, session['user']['username'])

        review = request.form['review']
        get_db().updateReview(id, review, session['user']['username'])
    else:
        return jsonify('Error: User not authenticated')

@app.route('/deletebook', methods=['GET'])
def deletebook():
    if 'user' in session:
        title = request.args.get('title')
        get_db().deleteBook(title, session['user']['username'])
        return render_template('/mybooks.html')
    else:
        return jsonify('Error: User not authenticated')


@app.route('/gettrendingbook', methods=['GET'])
def gettrendingbook():
    title = request.args.get('title')
    jsonFile = json.load()
    return render_template('/mybooks.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/')

if __name__ == "__main__":
    app.run(debug=True)