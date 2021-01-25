from flask import Flask, render_template, request ,send_file
import pafy
from pathlib import Path
import pytube
import time

app = Flask(__name__)
destination = str(Path.home() / "Downloads")


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/get_infos', methods=['POST', 'GET'])
def infos():
    url = request.json['url']
    video = pafy.new(url)
    return {'video':1 , 'title':video.title , 'author':video.author , 'duration':video.duration , 'image':video.getbestthumb() , 'loading':1}


@app.route('/get_infos_playlist', methods=['POST', 'GET'])
def infos_p():
    url = request.json['url']
    video = pafy.get_playlist(url)
    return { 'video':-1 , 'title':video['title'], 'author':video['author'] , 'items':len(video['items']), 'image':video['items'][0]['pafy'].getbestthumb() ,'loading':1}


@app.route('/playlist_video', methods=['POST'])
def playlist_v():
    url = request.json['url']
    test = pafy.get_playlist(url)
    all_videos = test['items']
    for item in all_videos:
        link = str(item['pafy'].watchv_url)
        stream =  pafy.new(link).streams
        length = len(pafy.new(link).streams)-1
        if stream[length].download(filepath=destination):
            continue
    return ""


@app.route('/playlist_audio', methods=['POST'])
def playlist_a():
    url = request.json['url']
    test = pafy.get_playlist(url)
    all_videos = test['items']
    for item in all_videos:
        link = str(item['pafy'].watchv_url)
        if pafy.new(link).getbestaudio(preftype="mp3"):
            continue
    return ""


@app.route('/video', methods=['POST'])
def video():
    url = request.json['url']
    source = pafy.new(str(url)).title + ".mp4"
    stream = pafy.new(str(url))
    # if stream.streams[ len(stream.streams)-1].download(filepath=destination):
    if pytube.YouTube(url).streams.first().download() :
        time.sleep(5)
        return ""
    return send_file(source)


@app.route('/audio', methods=['POST'])
def audio():
    url = request.json['url']
    source = pafy.new(str(url)).title + ".mp3"
    stream = pafy.new(str(url))
    if stream.getbestaudio().download(filepath=destination):
        pass
    return " "


if __name__ == '__main__':
    app.run()
