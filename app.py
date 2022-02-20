from flask import Flask, render_template, g, request, redirect
from database import DB
import os

# def main():

#     db = DB()

#     db.createUser("jacy", "jacy@gmail.com", "password")
#     data = db.getUser("jacy@gmail.com")

app = Flask(__name__, static_folder='public', static_url_path='')
secret_key = os.urandom(32)
app.config['SECRET_KEY'] = secret_key

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
    return render_template('/index.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        print(name + email + password)
        if name and email and password:
            get_db().createUser(name, email, password)
            return redirect('/')
    return render_template('/signup.html')

if __name__ == "__main__":
    app.run(debug=True)