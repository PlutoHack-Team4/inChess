from flask import Flask, redirect, url_for, render_template, request, session, flash
from datetime import timedelta
import pymongo
from pymongo import MongoClient
import uuid

app = Flask(__name__)
app.secret_key = "in-chess"
app.permanent_session_lifetime = timedelta(minutes=10)

# set up init cluster
cluster = MongoClient("mongodb+srv://adminTyler:QCKydFV5GFVBj4LH@cluster0.nce7s.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
# select database
db = cluster["inChest"]

# pages
@app.route("/")
def home():
    return render_template("index.html")
@app.route("/schedule")
def schedule():
    # check if authenticated
    return render_template("schedule.html")
@app.route("/leaderboard")
def lb():
    return render_template("leaderboard.html")


# sign in page
@app.route("/login", methods=["POST", "GET"])
def login():
    # if get request
    # if post request
    if request.method == "POST":
        session.permanent = True #session stays permanent for 10 mins
        # if the user logged in
        user = request.form["email"]
        session["user"] = user
        flash("Login Successful!")
        # if authenticated then log the user in
        # redirect to user page
        return redirect(url_for("user"))
    else:
        if "user" in session:
            flash("Login Successful!")
            return redirect(url_for("user"))
        return render_template("login.html")

# profile page
@app.route("/profile", methods=["POST", "GET"])
def user():
    email = None
    # check if user authenticated
    if "user" in session:
        user = session["user"]
        if request.method == "POST":
            email = request.form("email")
        return render_template("profile.html", user = user)
    # if no user logged in, redirect to login page
    else:
        flash("You are not logged in!")
        return redirect(url_for("login"))

# log out 
@app.route("/logout")
def logout():
    flash(f"You have been logged out!", "info")
    session.pop("user", None)
    return redirect(url_for("login"))

# sign up page
@app.route("/signup", methods=["POST", "GET"])
def signup():
    if "user" in session:
        flash("Login Successful!")
        return redirect(url_for("user"))
    else:
        if request.method == "POST":
            # get data back
            fname = request.form.get("fname")
            lname = request.form.get("lname")
            email = request.form.get("email")
            pw = request.form.get("password")
            level = request.form.get("comp_select")
            # select user collection
            collection = db["user"]
            #save to db
            collection.insert_one({
                "_id" : uuid.uuid4().hex,
                "fname" : fname,
                "lname" : lname,
                "email": email,
                "pw": pw,
                "level": level
            })
            return redirect(url_for("login"))
    return render_template("signup.html")

if __name__ == "__main__":
    app.run(debug=True)