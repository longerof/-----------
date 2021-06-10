from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from hashlib import sha256
from flask import session
import sqlite3

app = Flask(__name__)
app.secret_key = b"PaxomCraft"

@app.route("/fun/")
def main_fun():
    return render_template("base.html")

@app.route("/")
def main():
    return redirect("/auth")

@app.route("/auth")
def auth():
    login = None

    if "user" in session:
        login = session["user"]

    return render_template("auth.html", login=login)

@app.route("/fun/auth", methods = ["POST"])
def fun_auth():
    login = request.form["login"]
    password = sha256(request.form["password"].encode("utf-8")).hexdigest()

    f = open("users.info", "r")
    data = f.read()
    f.close()
    if login + "`" + password in data:
        session["user"] = login

    return redirect("/fun/")


@app.route("/reg")
def reg():
    return render_template("reg.html")

@app.route("/fun/reg", methods=["POST"])
def fun_reg():
    con = sqlite3.connect("да.db")
    cursor = con.cursor()

    sqlCheckLogin = cursor.execute("SELECT login FROM user WHERE login = ?", (request.form["login"],))
    checkLogin = sqlCheckLogin.fetchall()

    if len(checkLogin) != 0:
        return redirect("/fun/")

    login = request.form["login"]
    password = sha256(request.form["password"].encode("utf-8")).hexdigest()
    cursor.execute("INSERT INTO user (login, password) VALUES (?, ?)", (login, password))
    con.commit()

    return redirect("/fun/")
app.run()