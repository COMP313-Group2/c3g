# Flask web framework
from flask import Flask, render_template, g
# Database
import sqlite3
# from app import create_app

app = Flask(__name__)


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
def home():
    users = query_db('SELECT * FROM user')
    return render_template('index.html', users=users)

@app.route("/space_pong")
def space_pong():
    return render_template('space_pong/index.html')

@app.route("/blade_runner")
def blade_runner():
    return render_template('blade_runner/index.html')

@app.route("/excaliburs_quest")
def excaliburs_quest():
    return render_template('excaliburs_quest/index.html')

@app.route("/potato_tomato")
def potato_tomato():
    return render_template('potato_tomato/index.html')



















##################################################
# WebGL test

#    return """
#    <!doctype html>
#    <html>
#      <head>
#        <meta charset="utf-8">
#        <meta http-equiv="X-UA-Compatible" content="chrome=1" />
#        <meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1"></meta>
#        <style>
#            body {
#              text-align : center;
#            }
#            button {
#              display : block;
#              font-size : inherit;
#              margin : auto;
#              padding : 0.6em;
#            }
#        </style>
#      </head>
#    <body>
#        <p>[ Will detect WebGL after button press (below)]</p>
#        <button>Press here to detect WebGLRenderingContext</button>
#        <script type="text/javascript">
#            // Run everything inside window load event handler, to make sure
#            // DOM is fully loaded and styled before trying to manipulate it.
#            window.addEventListener("load", function() {
#              var paragraph = document.querySelector("p"),
#                button = document.querySelector("button");
#              // Adding click event handler to button.
#              button.addEventListener("click", detectWebGLContext, false);
#              function detectWebGLContext () {
#                // Create canvas element. The canvas is not added to the
#                // document itself, so it is never displayed in the
#                // browser window.
#                var canvas = document.createElement("canvas");
#                // Get WebGLRenderingContext from canvas element.
#                var gl = canvas.getContext("webgl")
#                  || canvas.getContext("experimental-webgl");
#                // Report the result.
#                if (gl && gl instanceof WebGLRenderingContext) {
#                  paragraph.textContent =
#                    "Congratulations! Your browser supports WebGL.";
#                } else {
#                  paragraph.textContent = "Failed to get WebGL context. "
#                    + "Your browser or device may not support WebGL.";
#                }
#              }
#            }, false);
#        </script>
#    </body> 
#    </html> 
#    """
