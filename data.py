from flask import Flask, render_template, g, request, redirect
from database import DB

# def main():

#     db = DB()

#     db.createUser("jacy", "jacy@gmail.com", "password")
#     data = db.getUser("jacy@gmail.com")

app = Flask(__name__)
app.secret_key = b'lkj98t&%$3rhfSwu3D'

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

@app.route('/signUp', methods=['GET', 'POST'])
def create_user():
    if request.method == 'POST':
        name = request.form['name']
        username = request.form['username']
        password = request.form['password']
        if name and username and password:
            get_db().create_user(name, username, password)
            return redirect('/index.html')
    return render_template('signUp.html')

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=8080, debug=True)