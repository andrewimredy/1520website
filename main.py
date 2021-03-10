from flask import Flask, render_template
app = Flask(__name__)

@app.route('/')
def homepage():
    return render_template("index.html")

#sending in the username will look like this
#@app.route('/')
#def homepage():
#    return render_template("index.html", user="name goes here")

@app.route('/Profile')
def profile_view():
    return render_template("profile.html")

@app.route('/myStats')
def stats_view():
    return render_template("myStats.html")

@app.route('/groups')
def groups_view():
    return render_template("groups.html")
