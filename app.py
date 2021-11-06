# Flask web framework
from flask import Flask, render_template, g, request, redirect, session, flash, send_file
from werkzeug.utils import secure_filename
from markupsafe import escape

import sqlite3 # Database
import re # Regular Expressions
import shutil # File operations
import os
import fileinput
import sys
import yagmail
import unittest


app = Flask(__name__, static_url_path='')
app.secret_key = b'148c8959c6ba9202c4d6a018d90554f53023a862f9e7ce136a6e30a6700e753c'



################################################################################
# Database Configuration and Helpers

# SQLite database storage file
DATABASE = 'database.db'

# Connect to SQLite and return dicts from db
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)

    def make_dicts(cursor, row):
        return dict((cursor.description[idx][0], value)
                    for idx, value in enumerate(row))

    db.row_factory = make_dicts
    return db


# Query helper function
def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv


# Db connection close helper function
@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


# Db schema and data initializer
def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()


init_db()



################################################################################
# Routes

@app.route("/")
def home_page():
    """Display the home page"""
    users = query_db('SELECT * FROM users')
    games = query_db('SELECT * FROM games')
    stars = query_db('SELECT gameId, AVG(star) FROM stars GROUP BY gameId')
    comments = query_db('SELECT * FROM comments ORDER BY date DESC')
    query = query_db('SELECT games.gameId, gameName, description, userName, AVG(star) FROM games LEFT OUTER JOIN stars ON games.gameId=stars.gameId INNER JOIN users ON games.userId=users.userId GROUP BY games.gameId ORDER BY AVG(star) DESC')
    return render_template('index.html', users=users, games=games, stars=stars, comments=comments, query=query)


def validate(text, pattern):
    """Validate data format is correct"""
    regex = re.compile(pattern, re.I)
    match = regex.match(request.form[text])
    return bool(match)


@app.route('/signup', methods=['GET', 'POST'])
def signup_page():
    """Allow the user to both see the signup form and signup"""
    if request.method == 'GET':
        return render_template('signup.html')

    elif request.method == 'POST':
        if (validate('name', '(\w| )+')
            and validate('email', '.+\@.+\..+')
            and validate('password', '(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{6,}')
            ):
            db = get_db()
            db.execute('INSERT INTO users (userName, role, email, password) VALUES (?, ?, ?, ?)',
                       tuple([request.form[val] for val in ['name', 'role', 'email', 'password']]))
            db.commit()
            flash('You have successfully signed up!')
            return redirect('/')
        else:
            flash('Invalid info has been sent to Flask')
            return redirect('/')


@app.route('/signin', methods=['GET', 'POST'])
def signin_page():
    """Allow the user to both see the signin form and signin"""
    if request.method == 'GET':
        return render_template('signin.html')

    elif request.method == 'POST':
        if (validate('email', '.+\@.+\..+')
            and validate('password', '(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{6,}')
            ):
            user = query_db('SELECT * FROM users WHERE email = ? AND password = ?',
                            (request.form['email'], request.form['password']), one=True)
            if user is None:
                flash('User does not exist')
                return redirect('/')
            else:
                session['user'] = user
                flash('You were successfully logged in')
                return redirect('/')
        else:
            flash('Invalid info has been sent to Flask')
            return redirect('/')


@app.route('/logout')
def logout_page():
    """Remove the user from being the currently logged on user"""
    session.pop('user', None)
    flash('You have successfully logged out')
    return redirect('/')

def replace(file, previousw, nextw):
    """Helper function for /user to modify uploaded files"""
    for line in fileinput.input(file, inplace=1):
        line = line.replace(previousw, nextw)
        sys.stdout.write(line)


@app.route('/user', methods=['GET', 'POST'])
def user_page():
    """Allow user to modify personal settings and to upload games to the server"""
    if 'user' in session and session['user']:
        if request.method == 'GET':
            return render_template('user.html')
        elif request.method == 'POST':
            f = request.files['file']

            # NOTE: change base when switching between local and remote development
            # base = "/home/hassan/repo/c3g/static/"
            base = "/home/public/c3g/static/"

            game_id = query_db('SELECT ifnull(max(userId), 0) FROM games;', one=True)['ifnull(max(userId), 0)'] + 1

            f.save(f"{base}{f.filename}")
            shutil.unpack_archive(f"{base}{f.filename}", f"{base}")
            os.remove(f"{base}{f.filename}")
            shutil.move(f"{base}{re.sub('.zip', '', f.filename)}", f"{base}game/{game_id}")


            replace(f"{base}game/{game_id}/index.html", 
                    '<link rel="shortcut icon" href="TemplateData/favicon.ico">',
                    f'<link rel="shortcut icon" href="{game_id}/TemplateData/favicon.ico">')

            replace(f"{base}game/{game_id}/index.html", 
                    '<link rel="stylesheet" href="TemplateData/style.css">',
                    f'<link rel="stylesheet" href="{game_id}/TemplateData/style.css">')

            replace(f"{base}game/{game_id}/index.html", 
                    '<script src="TemplateData/UnityProgress.js"></script>',
                    f'<script src="{game_id}/TemplateData/UnityProgress.js"></script>')

            replace(f"{base}game/{game_id}/index.html", 
                    '<script src="Build/UnityLoader.js"></script>',
                    f'<script src="{game_id}/Build/UnityLoader.js"></script>')

            replace(f"{base}game/{game_id}/index.html", 
                    'var gameInstance = UnityLoader.instantiate("gameContainer", "Build/',
                    f'var gameInstance = UnityLoader.instantiate("gameContainer", "{game_id}/Build/')

            replace(f"{base}game/{game_id}/index.html", 
                    'var unityInstance = UnityLoader.instantiate("unityContainer", "Build',
                    f'var unityInstance = UnityLoader.instantiate("unityContainer", "{game_id}/Build')

            replace(f"{base}game/{game_id}/index.html", 
                    'var buildUrl = "Build";',
                    f'var buildUrl = "{game_id}/Build";')


            db = get_db()
            db.execute('INSERT INTO games (gameId, userId, gameName, description) VALUES (?, ?, ?, ?)', 
                    (game_id, session['user']['userId'], re.sub('.zip', '', f.filename), request.form['description']))
            db.commit()

            flash('You have successfully added a game!')
            return render_template('user.html')
    else:
        flash('You are not authorized to access this page')
        return render_template('index.html')


@app.route("/game/<int:game_id>")
def game_page_api(game_id):
    """Send the index file (includes only iframe)"""
    return send_file(f'static/game/{game_id}/index.html')


@app.route("/play_game/<int:game_id>")
def play_game_page(game_id):
    """Send the complete webpage with iframe of game"""
    query = query_db(f'SELECT * FROM games INNER JOIN users ON games.userId = users.userId WHERE games.gameId = {game_id}')
    comments = query_db(f'SELECT * FROM comments INNER JOIN users ON comments.userId = users.userId WHERE gameId = {game_id} ORDER BY date DESC')
    return render_template('game.html', query=query, comments=comments)


@app.route("/rate_game/<int:game_id>/<int:star>", methods=['POST'])
def rate_game_api(game_id, star):
    """Allow user to rate a particular game with a value"""
    if 'user' in session and session['user']:
        query = query_db(f'SELECT * FROM stars WHERE userId = {session["user"]["userId"]} AND gameId = {game_id}')
        if query != []:
            # update
            db = get_db()
            db.execute(f'UPDATE stars SET star = {star} WHERE userId = {session["user"]["userId"]} AND gameId = {game_id}')
            db.commit()
        else: 
            # insert
            db = get_db()
            db.execute('INSERT INTO stars (userId, gameId, star) VALUES (?, ?, ?)', 
                    (session['user']['userId'], game_id, star))
            db.commit()
        return redirect(f'/play_game/{game_id}')
    else:
        return "You must be logged in to rate a game", 500


@app.route("/comment_game/<int:game_id>", methods=['POST'])
def comment_game_api(game_id):
    """Allow the user to comment on a particular game"""
    if 'user' in session and session['user']:
        db = get_db()
        db.execute('INSERT INTO comments (userId, gameId, comment) VALUES (?, ?, ?)', 
                (session['user']['userId'], game_id, request.form['comment']))
        db.commit()
        return redirect(f'/play_game/{game_id}')
    else:
        return "You must be logged in to rate a game", 500


@app.route("/forgot_password", methods=['GET', 'POST'])
def forgot_password_page():
    """Allow the user to change a forgotten password"""
    if request.method == 'GET':
        return render_template('forgot_password.html')

    elif request.method == 'POST':
        user = query_db(f'SELECT * FROM users WHERE email = "{request.form["email"]}"', one=True)
        yagmail.SMTP('hassan149367@gmail.com', 'WMP4s4SgC2syEqa').send(user['email'], 
                'Forgot Password for Titan Games', 
                f'Hello {user["userName"]}, it seems you forgot your password. To reset your password, click the following link: <a href="https://c3g.nfshost.com/reset_password/{user["userId"]}">Reset Password</a>.')
        flash('Email has been sent!')
        return redirect('/')


@app.route("/reset_password/<int:user_id>", methods=['GET', 'POST'])
def reset_password_page(user_id):
    """Reset password based on forgotten password link"""
    if request.method == 'GET':
        return render_template('reset_password.html', user_id=user_id)

    elif request.method == 'POST':
        db = get_db()
        db.execute(f'UPDATE users SET password = "{request.form["password"]}" WHERE userId = {user_id}')
        db.commit()
        flash('Password has been updated!')
        return redirect('/')


@app.route("/search", methods=['POST'])
def search_page():
    """Allow the user to search for a particular game"""
    if request.method == 'POST':
        q = " OR ".join([f'gameName LIKE "%{x}%"' for x in request.form['search'].split()])
        query = query_db('SELECT games.gameId, gameName, description, userName, AVG(star) FROM games LEFT OUTER JOIN stars ON games.gameId=stars.gameId INNER JOIN users ON games.userId=users.userId WHERE ' + q + ' GROUP BY games.gameId ORDER BY AVG(star) DESC')
        return render_template('search.html', query=query)


@app.route("/delete")
def delete_page():
    """Allow the user to delete their account"""
    db = get_db()
    db.execute(f'DELETE FROM users WHERE userId = {session["user"]["userId"]}')
    db.commit()
    session.pop('user', None)
    flash("Your account has been deleted. We're sad to see you go.")
    return redirect('/')


class Tests(unittest.TestCase):
    def query_db(string):
        con = sqlite3.connect("database.db")
        cur = con.cursor()
        x = [row for row in cur.execute(string)]
        con.close()
        return x

    def test_password(self):
        regex = re.compile('(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{6,}', re.I)
        match = regex.match('Password0)')
        self.assertTrue(bool(match))

    def test_db_empty(self):
        init_db() # reset db
        users = Tests.query_db('SELECT * FROM users;')
        self.assertEqual(users, [])
        games = Tests.query_db('SELECT * FROM games;')
        self.assertEqual(games, [])


    def test_db_insert(self):
        init_db() # reset db
        con = sqlite3.connect("database.db")
        cur = con.cursor()
        cur.execute('INSERT INTO users values (1,"hassan","dev","hassan@gmail.com","Password0)")')
        con.commit()
        users = Tests.query_db('SELECT * FROM users')
        self.assertEqual(len(users), 1)

    def test_db_average_stars(self):
        init_db() # reset db
        con = sqlite3.connect("database.db")
        cur = con.cursor()
        cur.execute('INSERT INTO stars (userId, gameId, star) values (1,1,5)')
        cur.execute('INSERT INTO stars (userId, gameId, star) values (2,1,4)')
        cur.execute('INSERT INTO stars (userId, gameId, star) values (3,2,1)')
        con.commit()
        stars = Tests.query_db('SELECT AVG(star) FROM stars GROUP BY gameId')
        self.assertEqual(stars[0][0], 4.5)

    def test_db_update_stars(self):
        init_db() # reset db
        con = sqlite3.connect("database.db")
        cur = con.cursor()
        cur.execute('INSERT INTO users values (1, "hassan", "dev", "hassan@gmail.com", "Password0)")')
        cur.execute('INSERT INTO games values (1, 1, "Space Pong", "Pong, with a space theme")')
        con.commit()
        join = Tests.query_db(f'SELECT * FROM games INNER JOIN users ON games.userId = users.userId')
        self.assertEqual(join[0][2], "Space Pong")
        self.assertEqual(join[0][5], "hassan")


# Run the unit tests if called using python3 app.py
if __name__ == '__main__':
    unittest.main()
