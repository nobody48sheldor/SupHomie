# import os
# import sys
from datetime import datetime
import requests
from flask import Flask, render_template, request, url_for, redirect
from dotenv import load_dotenv

load_dotenv("./.flaskenv")

app = Flask(__name__)
# app.config['SECRET_KEY'] = os.urandom(24).hex()

H = [" "," "," "," "," "]
USER = [""]
DAY = ["", ""]
Cont = {'history': H, 'user': USER, 'day': DAY}


@app.route("/")
def index():
    user = "Arnaud"
    USER[0] = user
    date = str(datetime.today().strftime('%Y-%m-%d'))
    last = date[-1]
    print(date[-2:])
    if int(date[-2:]) < 10:
        date = date[0:-2]
        date = date + last
        day =date[-1]
    else:
        day = date[-2:]
    DAY[0] = str(date)
    DAY[1] = str(day)
    print(day)
    print('https://ssl.gstatic.com/calendar/images/dynamiclogo_2020q4/calendar_' + Cont['day'][1] + '_2x.png')
    return( render_template("index.html", Cont=Cont) )

@app.route("/", methods=["GET", "POST"])
def search():
    searched = request.form["searched"]
    H.append(searched)
    return(redirect("https://www.google.com/search?client=firefox-b-d&q={}".format(searched)))

@app.route("/todo-widget")
def todo():
    return( render_template("todo.html") )


if __name__ == "__main__":
    app.run(debug=True)
