from flask import Blueprint, request, session, redirect, render_template
from google.cloud import datastore

from user import userStore, generate_creds, hash_password

blue = Blueprint('auth', __name__)

datastore = datastore.Client()
userstore = userStore(datastore)

@blue.route("/login" , methods=["GET"])
def show_login():
    user = get_user()
    if user:
        redirect("/")
    return render_template("login.html", auth = True)

@blue.route("/login", methods=["POST"])
def handle_login():
    username = request.form.get("username")
    password = request.form.get("password")
    user = userstore.verify_password(username, password)
    if not user:
        return render_template("login.html", auth=True, error="Password did not match.")
    session["user"] = user.username
    return redirect("/")

@blue.route("/logout")
def handle_logout():
    session.clear()
    return redirect("/")

@blue.route("/signup" , methods=["GET"])
def show_signup():
    user = get_user()
    if user:
        redirect("/")
    return render_template("signup.html", auth = True)

@blue.route("/signup" , methods=["POST"])
def handle_signup():
    username = request.form.get("username")
    password = request.form.get("password")
#    if username in userstore.list_existing_users():
#        return render_template(
#            "signup.html", auth=True, error="A user with that username already exists"
#        )
    userstore.store_new_credentials(generate_creds(username, password))
    session["user"] = username
    return redirect("/")

def get_user():
    return session.get("user", None)