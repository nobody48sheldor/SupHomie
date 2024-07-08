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

def get_news(number=5, squery="World News"):
    news = [[] for i in range(number)]
    google_news = GNews(language='en', period='4d', max_results=number, exclude_websites=['yahoo.com'])
    json_resp = google_news.get_news(squery)
        
    for i in range(number):
        news[i].append(json_resp[i]['title'])
        news[i].append(json_resp[i]['published date'])
        news[i].append(json_resp[i]['url'])
        news[i].append(json_resp[i]['publisher']['title'])
        news[i].append("")
    return(news)

def get_summary(url, number=5):
    google_news = GNews(language='en', period='4d', max_results=number, exclude_websites=['yahoo.com'])
    text = str(google_news.get_full_article(url))

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
    cmd = """curl http://localhost:11434/api/generate -d '{"model": "mistral", "prompt": " """ + "sumarize in LESS THAN 70 WORDS the following text : " + text + """ ", "stream": false }'"""

    print(cmd)

    with tempfile.TemporaryFile() as tempf:
        proc = subprocess.Popen(cmd, stdout=tempf,shell=True)
        proc.wait()
        tempf.seek(0)
        m = str(tempf.read())[79::]

    m_ = ""
    for i in m:
        if i != '[':
            m_ += i
        else:
            break

    m=m_[:-24]
    m=m_[:-45]
    if m == "":
        return("Failed, ollama is not running")

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
    return( render_template("news.html", value=latest_news) )

@app.route("/news", methods=["GET", "POST"])
def news_news():
    url = request.form.get("news",None)
    new_index = request.form.get("switch",None)
    query = request.form.get("query",None)
    if url !=  None:
        print(url)
        summary = get_summary(url)
        latest_news[ latest_news[6][0] ][4] = summary
    if new_index != None:
        print(new_index)
        current = int( new_index )
        latest_news[6][0] = current
    if query != None:
        news_temp = get_news(squery = query)
        current = 0
        news_temp.append( [len(news_temp)] )
        news_temp.append( [current] )
        for i in range(len(news_temp)):
            latest_news[i] = news_temp[i]
        for i in latest_news:
            print(i)
    return( render_template("news.html", value=latest_news) )




if __name__ == "__main__":
    app.run(debug=True)
