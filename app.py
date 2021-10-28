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


# init_db()



################################################################################
# Routes

@app.route("/")
def home_page():
    users = query_db('SELECT * FROM users')
    games = query_db('SELECT * FROM games')
    stars = query_db('SELECT gameId, AVG(star) FROM stars GROUP BY gameId')
    query = query_db('SELECT * FROM games INNER JOIN users ON games.userId=users.userId')
    return render_template('index.html', users=users, games=games, stars=stars, query=query)


# Validate data format is correct
def validate(text, pattern):
    regex = re.compile(pattern, re.I)
    match = regex.match(request.form[text])
    return bool(match)


# Show signup form and process and save returned form data
@app.route('/signup', methods=['GET', 'POST'])
def signup_page():
    if request.method == 'GET':
        return render_template('signup.html')

    elif request.method == 'POST':
        if (validate('name', '(\w| )+')
            and validate('email', '.+\@.+\..+')
            and validate('password', '(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{6,}')
            ):
            db = get_db()
            db.execute('INSERT INTO users (userName, email, password) VALUES (?, ?, ?)',
                       tuple([request.form[val] for val in ['name', 'email', 'password']]))
            db.commit()
            flash('You have successfully signed up!')
            return redirect('/')
        else:
            flash('Invalid info has been sent to Flask')
            return redirect('/')


# Show signin form and return user if found
@app.route('/signin', methods=['GET', 'POST'])
def signin_page():
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
    session.pop('user', None)
    flash('You have successfully logged out')
    return redirect('/')

def replace(file, previousw, nextw):
   for line in fileinput.input(file, inplace=1):
       line = line.replace(previousw, nextw)
       sys.stdout.write(line)


@app.route('/user', methods=['GET', 'POST'])
def user_page():
    if 'user' in session and session['user']:
        if request.method == 'GET':
            return render_template('user.html')
        elif request.method == 'POST':
            f = request.files['file']

            # f.filename = Blade Runner.zip
            # filename_snake = blade_runner.zip
            # folder = Blade Runner
            # folder_snake = blade_runner

            # filename_snake = re.sub('\s', '_', secure_filename(f.filename.lower()))
            # folder = re.sub('_', ' ', re.sub('.zip', '', secure_filename(f.filename)))
            # folder_snake = re.sub('.zip', '', filename_snake) # TODO remove

            # NOTE: change base when switching between local and remote development
            base = "/home/hassan/repo/c3g/static/"
            # base = "/home/public/c3g/static/"

            game_id = query_db('SELECT ifnull(max(userId), 0) FROM games;')[0]['ifnull(max(userId), 0)'] + 1

            f.save(f"{base}{f.filename}")
            shutil.unpack_archive(f"{base}{f.filename}", f"{base}")
            os.remove(f"{base}{f.filename}")
            shutil.move(f"{base}{re.sub('.zip', '', f.filename)}", f"{base}game/{game_id}")

            # replace(f"{base}game/{game_id}/index.html", 
            #         'TemplateData', 
            #         # f'static/game/{game_id}/TemplateData')
            #         f'{game_id}/TemplateData')

            # replace(f"{base}game/{game_id}/index.html", 
            #         'Build', 
            #         # f'static/game/{game_id}/Build')
            #         f'{game_id}/Build')

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
            db.execute('INSERT INTO games (gameId, userId, gameName) VALUES (?, ?, ?)', 
                    (game_id, session['user']['userId'], re.sub('.zip', '', f.filename)))
            db.commit()

            flash('You have successfully added a game!')
            return render_template('user.html')
    else:
        flash('You are not authorized to access this page')
        return render_template('index.html')


# Games (Built-in)
# @app.route("/space_pong")
# def space_pong():
#     return render_template('space_pong/index.html')

# @app.route("/excaliburs_quest")
# def excaliburs_quest():
#     return render_template('excaliburs_quest/index.html')

# @app.route("/potato_tomato")
# def potato_tomato():
#     return render_template('potato_tomato/index.html')

# # Dynamically added Games
# @app.route("/blade_runner")
# def blade_runner2():
#     return send_file('static/game/1/index.html')

@app.route("/game/<int:game_id>")
def game_page(game_id):
    return send_file(f'static/game/{game_id}/index.html')


@app.route("/play_game/<int:game_id>")
def play_game_page(game_id):
    query = query_db(f'SELECT * FROM games INNER JOIN users ON games.userId=users.userId WHERE games.gameId = {game_id}')
    return render_template('game.html', query=query)


@app.route('/rate_game/<int:game_id>/<int:star>', methods=['POST'])
def rate_game(game_id, star):
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
