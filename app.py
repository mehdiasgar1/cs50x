import hashlib
import csv
from functools import wraps
from flask import Flask, flash, redirect, render_template, request, session, url_for
#from flask_session import Session
#from tempfile import mkdtemp
#from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError

# Configure application
app = Flask(__name__)
app.secret_key = 'Messi'
# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('loggedIn'):
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function


@app.route("/", methods=['POST', 'GET'])
def welcome():
    if request.method == 'POST':
        pass
    else:
        pass

    return render_template("index.html")
    # return render_template("afterlog.html", name='ali')


@app.route("/index", methods=['POST', 'GET'])
@login_required
def index():
    if request.method == 'POST':
        pass
    else:
        pass
    return render_template("main.html", name=session.get("userName"))


@app.route("/signup", methods=["POST", "GET"])
def pgsigUp():
    if request.method == 'POST':
        userName = request.form.get('username')
        passWord = request.form.get('pass')
        if (signUp(userName, passWord)):
            return redirect("/")
        else:
            return redirect("/error")
    else:
        return render_template("signup.html")


@app.route("/login", methods=['POST', 'GET'])
def loginPG():
    if request.method == 'POST':
        userName = request.form.get('username')
        passWord = request.form.get('pass')
        if (passcheck(userName, passWord)):

            return redirect("/index")
        else:
            return redirect("/error")
    else:
        return render_template("login.html")


@app.route("/error")
def errorfunc():
    return render_template("error.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


def passwordHash(password):
    hashed = hashlib.sha256(str(password).encode('utf-8')).hexdigest()
    return hashed


def passcheck(userName, passWord):
    dbTemp = {}
    with open('database.csv', 'r') as f:
        for line in f:
            dbTemp[line.strip().split(',')[0]] = line.strip().split(',')[1]
    if userName in dbTemp.keys():
        if passwordHash(passWord) == dbTemp[userName]:
            session['loggedIn'] = True
            session['userName'] = userName
            return True
        else:
            return False
    else:
        return False


def signUp(userName, passWord):
    dbTemp = {}
    with open('database.csv', 'r') as f:
        for line in f:
            dbTemp[line.strip().split(',')[0]] = line.strip().split(',')[1]
    if (userName in dbTemp.keys()):
        return False
    if passWord == '':
        return False
    with open('database.csv', 'a')as f:
        f.write(userName+','+passwordHash(passWord)+'\n')
    return True


if __name__ == '__main__':
    app.run(debug=True)
# @app.route("/sighup", methods=["GET", "POST"])
