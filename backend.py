import os
import sys
from datetime import datetime
import requests
from flask import Flask, render_template, request, url_for, redirect
from dotenv import load_dotenv
from gnews import GNews
import tempfile
import subprocess

load_dotenv("./.flaskenv")

app = Flask(__name__)
# app.config['SECRET_KEY'] = os.urandom(24).hex()




    # news

def get_news(number=5, query="World News"):
    latest_news = [[] for i in range(number)]
    google_news = GNews(language='en', period='4d', max_results=number, exclude_websites=['yahoo.com'])
    json_resp = google_news.get_news(query)
        
    for i in range(number):
        latest_news[i].append(json_resp[i]['title'])
        latest_news[i].append(json_resp[i]['published date'])
        latest_news[i].append(json_resp[i]['url'])
        latest_news[i].append(json_resp[i]['publisher']['title'])
        latest_news[i].append("")
    return(latest_news)

def get_summary(url, number=5):
    google_news = GNews(language='en', period='4d', max_results=number, exclude_websites=['yahoo.com'])
    text = str(google_news.get_full_article(url))
    print(text)

    text = text.replace('"', ' ')
    text = text.replace("'", ' ')
    text = text.replace("’", ' ')
    text = text.replace("‘", ' ')
    text = text.replace("$", ' ')
    text = text.replace("%", ' in pourcent ')
    text = text.replace("“", ' ')
    text = text.replace("”", ' ')
    text = text.replace("\n", ' ')

    #os.system("ollama start &")
    cmd = """curl http://localhost:11434/api/generate -d '{"model": "mistral", "prompt": " """ + "sumarize in LESS THAN 100 WORDS the following text : " + text + """ ", "stream": false }'"""

    print(cmd)

    with tempfile.TemporaryFile() as tempf:
        proc = subprocess.Popen(cmd, stdout=tempf,shell=True)
        proc.wait()
        tempf.seek(0)
        m = str(tempf.read())[79::]
        print()

    m_ = ""
    for i in m:
        if i != '[':
            m_ += i
        else:
            break

    m=m_[:-24]
    m=m_[:-45]
    print(m)

    #os.system("killall ollama")
    return( m )

# route / (index)

@app.route("/")
def index(user_prompt="Hi Arnaud !"):
    USER[0] = user_prompt
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



# variables


H = [" "," "," "," "," "]
USER = [""]
DAY = ["", ""]
Cont = {'history': H, 'user': USER, 'day': DAY, 'summary': "Summary !"}
current = 0

latest_news = get_news()
latest_news.append( [len(latest_news)] )
latest_news.append( [0] )






# route /todo-widget (todo)

@app.route("/todo-widget")
def todo():
    return( render_template("todo.html") )



# route /news (news)

@app.route("/news")
def news():
    latest_news = get_news()
    size = len(latest_news)
    latest_news.append([size])
    latest_news.append([current])
    print(latest_news)
    return( render_template("news.html", value=latest_news) )

@app.route("/news", methods=["GET", "POST"])
def news_news():
    url = request.form.get("news",None)
    new_index = request.form.get("switch",None)
    if url:
        print(url)
        summary = get_summary(url)
        latest_news[ latest_news[6][0] ][4] = summary
    if new_index != None:
        print(new_index)
        current = int( new_index )
        latest_news[6][0] = current
    return( render_template("news.html", value=latest_news) )




if __name__ == "__main__":
    app.run(debug=True)
