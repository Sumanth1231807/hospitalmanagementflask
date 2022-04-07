from flask import Flask, request, render_template, flash
import sqlite3 as s

from werkzeug.utils import redirect

connection = s.connect("Hospital.db", check_same_thread=False)

listoftables = connection.execute("SELECT NAME FROM sqlite_master WHERE type='table' AND name= 'PATIENT'").fetchall()

if listoftables != []:
    print("Table Already Exist")
else:
    connection.execute('''CREATE TABLE PATIENT(
                        ID INTEGER PRIMARY KEY AUTOINCREMENT,
                        NAME TEXT,
                        MOBILE TEXT,
                        AGE INTEGER,
                        ADDRESS TEXT,
                        DOB TEXT,
                        PLACE TEXT,
                        PINCODE INTEGER
                       )''')

    print("Table Created Successfully")

App = Flask(__name__)


@App.route("/", methods=['GET', 'POST'])
def home():
    if request.method == "POST":
        getUname = request.form["uname"]
        getPass = request.form["pass"]
        if getUname == "admin" and getPass == "12345":
            return redirect('/dash')


    return render_template("home.html")


@App.route('/dash', methods=['GET', 'POST'])
def dashboard():
    if request.method == "POST":
        getName = request.form["name"]
        getMno = request.form["mno"]
        getAge = request.form["age"]
        getAddress = request.form["add"]
        getDob = request.form["dob"]
        getPlace= request.form["place"]
        getPin = request.form["pin"]


        connection.execute("INSERT INTO PATIENT(NAME, MOBILE, AGE, ADDRESS, DOB, PLACE, PINCODE) \
                VALUES('" + getName + "', '" + getMno + "', " + getAge + ", '" + getAddress + "', \
                '" + getDob + "', '" + getPlace + "', " + getPin + ")")
        connection.commit()
        print("Inserted Successfully")



        return redirect('/view')


    return render_template("dashboard.html")


@App.route('/view')
def viewAll():
    cursor = connection.cursor()
    count = cursor.execute("SELECT * FROM PATIENT")

    result = cursor.fetchall()
    return render_template("viewall.html", patient=result)



@App.route('/search', methods=['GET', 'POST'])
def search():
    cursor = connection.cursor()
    if request.method == "POST":
        getMno = request.form["mno"]
        count = cursor.execute("SELECT * FROM PATIENT WHERE MOBILE="+getMno)
        result = cursor.fetchall()
        if result is None:
            print("Mobile Number Not Exist")
        else:
            return render_template("search.html", search=result, status=True)
    else:
        return render_template("search.html", search=[], status=False)




@App.route('/up', methods=['GET', 'POST'])
def update():
    global getNMno
    cursor = connection.cursor()
    if request.method == "POST":
        getNMno = request.form["mno"]
        return redirect('/update')

    return render_template("update.html")


@App.route('/update', methods=['GET', 'POST'])
def updation():
    if request.method == "POST":
        getName = request.form["name"]
        getMno = request.form["mno"]
        getAge = request.form["age"]
        getAddress = request.form["add"]
        getDob = request.form["dob"]
        getPlace = request.form["place"]
        getPin = request.form["pin"]

        connection.execute("UPDATE PATIENT SET NAME='"+getName+"', MOBILE='"+getMno+"', AGE="+getAge+",\
         ADDRESS='"+getAddress+"', DOB='"+getDob+"', PLACE='"+getPlace+"', PINCODE='"+getPin+"' WHERE MOBILE='"+getNMno+"'")
        connection.commit()
        print("Updated Successfully......")

        return redirect('/view')

    return render_template("updation.html")


@App.route('/delete', methods=['GET', 'POST'])
def deletion():
    if request.method == "POST":
        getMno = request.form["mno"]
        connection.execute(" DELETE FROM PATIENT WHERE MOBILE='" + getMno + "'")
        connection.commit()
        print("Deleted Successfully")
        return redirect('/view')
    return render_template("delete.html")


@App.route('/cardview')
def cards():
    cursor = connection.cursor()
    count = cursor.execute("SELECT * FROM PATIENT")

    result = cursor.fetchall()
    return render_template("cards.html", patient=result)


if __name__ == "__main__":
    App.run(debug=True)