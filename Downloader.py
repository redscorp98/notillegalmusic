from __future__ import unicode_literals
import youtube_dl
import urllib.request
import urllib.parse
import re
import eyed3
import os
import subprocess 
from subprocess import call
default = 'default'
check = []
q = 0

def download(artist, title, track_num, album_artist, album, playlistname):
    filename = setfilename(title,artist)
    hold = album
    #cwd = os.getcwd() + "/output/" #os.getcwd() returns the current diretory
    output_folder = os.getcwd() + "\\" + 'output' + "\\"
    query_string = urllib.parse.urlencode({"search_query" : artist + " " + title})  #where the user input
    html_content = urllib.request.urlopen("http://www.youtube.com/results?" + query_string)
    search_results = re.findall(r'href=\"\/watch\?v=(.{11})', html_content.read().decode())
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download(['http://www.youtube.com/watch?v=' + search_results[0]])
    audiofile = eyed3.load(output_folder+"NA.mp3")
    audiofile.tag.artist = artist
    audiofile.tag.album = album
    audiofile.tag.album_artist = album_artist
    audiofile.tag.title = title
    audiofile.tag.track_num = track_num
    audiofile.tag.save()
    os.rename(output_folder+"NA.mp3", output_folder+filename)

ydl_opts = {
    'outtmpl' : '/' + 'output' + '/%(default)s.%(ext)s', 'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }], 'output':'video'
}

def setfilename(back, lead):
    global check, q
    collect = lead + " - " + back
    if q>0:
        for x in range (q):#reads 0 upto q
            if check[x] == collect:
                print("%d" % x)
                print("Repeated file: %s\n" % collect)
                collect += "(1)"
    check.append(collect)
    q+=1
    filename = collect +'.mp3'
    return filename