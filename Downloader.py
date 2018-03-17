from __future__ import unicode_literals
import youtube_dl as yt_dl, urllib, re, eyed3, os, subprocess
from subprocess import call

def download(artist, title, track_num, album_artist, album, playlistname):
    song = Downloader() # not sure how best to call the object???
    filename = song.combine(title,artist)
    output_folder = os.getcwd() + "\\" + playlistname + "\\"  #should i make this global rather than have it done every time the function is called?
                                                              #dunno uno, we think different innit
    if not(os.path.isfile(os.getcwd()+ "\\"+playlistname+"\\"+filename+".mp3")):
        print("Download Begin ("+filename+")")
        query_string = urllib.parse.urlencode({"search_query" : artist + " " + title})  #where the user input
        html_content = urllib.request.urlopen("http://www.youtube.com/results?" + query_string)
        search_results = re.findall(r'href=\"\/watch\?v=(.{11})', html_content.read().decode())
        ydl = yt_dl.YoutubeDL(song.ydl_config(playlistname,filename))
        ydl.download(['http://www.youtube.com/watch?v=' + search_results[0]])
        audio = eyed3.load(output_folder+filename+".mp3")#should i make tagging a object?
        audio.tag.artist = artist
        audio.tag.album = album
        audio.tag.album_artist = album_artist
        audio.tag.title = title
        audio.tag.track_num = track_num
        audio.tag.save()
        print("Complete")
    else:
        print("File found in directory... ("+filename+")")


class Downloader(object):
    def ydl_config(self,playlistname, filename):
        ydl_opts = {'quiet':True, 'outtmpl' : '/' + playlistname + '/'+filename+'.%(ext)s', 'format': 'bestaudio/best',
                'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',}], 'output':'video'}
        return ydl_opts

    def combine(self,back, lead):
        collect = lead + " - " + back
        return collect
