from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def home():
    return render_template('index.html')

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
