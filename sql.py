import sqlite3

con = sqlite3.connect("да.db")
cursor = con.cursor()

arrUser = cursor.execute("SELECT * FROM user")
users = arrUser.fetchall()
print(users)

login = input("login: ")
password = input("password: ")

cursor.execute(f"INSERT INTO user (login, password) VALUES (?, ?)", (login, password))
con.comit()