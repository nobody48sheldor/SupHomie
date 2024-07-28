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


def list_to_dict(l):
    d = {}
    lenght = len(l)
    for i in range(lenght):
        d[l[i]] = [l[ (i-1)%lenght ], l[ (i+1)%lenght ]]
    return(d)

playlist_list_1 = ["Into Yesterday.mp3", "$NOT - BLUE MOON (feat. Teddi Jones) [Official Audio].mp3", "Just Say Yes.mp3", "The Beach Boys - Big Sur (Audio).mp3"]
playlist_list_2 = ["Madvillain - All Caps.mp3", "Chumbawamba- Tubthumping.mp3", "Beer Goggles.mp3"]
playlists = {"my_playlist1": list_to_dict(playlist_list_1), "my_playlist2": list_to_dict(playlist_list_2)}


def tts(text, article_title):
    tts = gTTS(text=text, lang='en')
    tts.save('/home/arnaud/Desktop/arnaud/code/web/SupHomie/SupHomie/static/summaries/'+article_title+'.mp3')

def index_of(l, element):
    index = 0
    for i in range(len(l)):
        if l[index] == element:
            return(index)
        index += 1
    return("error")

def get_song(name):
    cmd = "yt-dlp -x --audio-format mp3 'ytsearch: "+name+"' -o '/home/arnaud/Desktop/arnaud/code/web/SupHomie/SupHomie/static/music/%(title)s.%(ext)s'"
    os.system(cmd)
    musics = os.listdir("/home/arnaud/Desktop/arnaud/code/web/SupHomie/SupHomie/static/music/")

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

    tts(m,m[:20])

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
def index_search():
    searched = request.form.get("searched", None)
    search_song= request.form.get("song",None)
    change_song = request.form.get("change-song",None)
    if searched != None:
        H.append(searched)
        return(redirect("https://www.google.com/search?client=firefox-b-d&q={}".format(searched)))
    if search_song != None:
        print()
        print()
        print(search_song)
        print()
        print()
        get_song(search_song)
        return(index())
    if  change_song != None:
        if change_song == "next":
            Cont["current_music"] = plau_next_song()
        if change_song == "previous":
            Cont["current_music"] = play_previous_song()
        return(index())
    return(index())



# variables

musics = os.listdir("/home/arnaud/Desktop/arnaud/code/web/SupHomie/SupHomie/static/music/")

H = [" "," "," "," "," "]
USER = [""]
DAY = ["", ""]
Cont = {'history': H, 'user': USER, 'day': DAY, 'summary': "Summary !", 'musics': musics, "current_music": 0, 'play': 0, 'playlists': ["all_musics" ,"my_playlist1", "my_playlist2"], "playlist_playing": "all_musics"}
current = 0

latest_news = get_news()
latest_news.append( [len(latest_news)] )
latest_news.append( [0] )


def play_next_song():
    musics = os.listdir("/home/arnaud/Desktop/arnaud/code/web/SupHomie/SupHomie/static/music/")
    Cont["musics"] = musics
    if Cont["playlist_playing"] == "all_musics":
        Cont["current_music"] = (Cont["current_music"] + 1 )%(len(Cont["musics"]))
    else:
         index_new = index_of( musics, playlists[ Cont["playlist_playing"] ][ str(musics[ Cont["current_music"] ]) ][1] )
         if index_new != "error":
             Cont["current_music"] = index_new

def play_previous_song():
    musics = os.listdir("/home/arnaud/Desktop/arnaud/code/web/SupHomie/SupHomie/static/music/")
    Cont["musics"] = musics
    if Cont["playlist_playing"] == "all_musics":
        Cont["current_music"] = (Cont["current_music"] - 1 )%(len(Cont["musics"]))
    else:
         index_new = index_of( musics, playlists[ Cont["playlist_playing"] ][ str(musics[ Cont["current_music"] ]) ][0] )
         if index_new != "error":
             Cont["current_music"] = index_new





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


# route /music (music)

@app.route("/music")
def music(play=0):
    Cont["play"] = play
    return( render_template("music.html", Cont=Cont) )

@app.route("/music", methods=["GET", "POST"])
def music_music():
    search_song= request.form.get("song",None)
    change_song = request.form.get("change-song",None)
    next_song = request.form.get("next_song",None)
    playbutton = request.form.get("playbutton",None)
    playlist_play = request.form.get("play_playlist",None)
    playlist_edit = request.form.get("edit",None)
    playlist = request.form.get("playlist",None)
    if playbutton != None:
        if playbutton == "play":
            return(music(1))
        if playbutton == "pause":
            return(music())
    if search_song != None:
        get_song(search_song)
        musics = dir_list = os.listdir("/home/arnaud/Desktop/arnaud/code/web/SupHomie/SupHomie/static/music/")
        Cont['musics'] = musics
        return(music())
    if change_song != None:
        print(str(change_song))
        if str(change_song) == "next":
            play_next_song()
            print(Cont["play"])
            if Cont["play"] == 1:
               return(music(1))
            else:
               return(music())
        if str(change_song) == "previous":
            play_previous_song()
            if Cont["play"] == 1:
               return(music(1))
            else:
               return(music())
    if next_song != None:
        print("\n\n\n song \n\n\n")
        Cont["current_music"] = next_song()
        return(music(1))
    if playlist_play != None:
        if playlist != None:
            musics = os.listdir("/home/arnaud/Desktop/arnaud/code/web/SupHomie/SupHomie/static/music/")
            Cont["playlist_playing"] = str(playlist)
            if str(playlist) == "all_musics":
                pass
            else:
                Cont["current_music"] = index_of( musics, list(playlists[ str(playlist) ].keys())[0] )
            return(music(1))
        return(music())
    if playlist_edit != None:
        if playlist != None:
            return(music())



if __name__ == "__main__":
    app.run(debug=True)
