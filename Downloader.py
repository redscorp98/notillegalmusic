from __future__ import unicode_literals
import youtube_dl, urllib, re, eyed3, os, subprocess 
from subprocess import call

default = 'default'#literally is a placeholder not sure if the variable does anything
check = []
q = 0
downloaded =0

def download(artist, title, track_num, album_artist, album, playlistname, number_items):
    filename = setfilename(title,artist)
    global q, downloaded
    #cwd = os.getcwd() + "/output/" #os.getcwd() returns the current diretory
    output_folder = os.getcwd() + "\\" + 'NA' + "\\"  #should i make this global rather than have it done every time the function is called?
    if not(os.path.isfile(output_folder+filename)) and not(os.path.isfile(os.getcwd()+ "\\"+playlistname+"\\"+filename)):
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
    if not(os.path.isfile(os.getcwd()+'\\Artwork\\'+album+'.jpg')):
        os.system('sacad "'+artist+'" "' + album+ '" 600 "' + os.getcwd() +'\\Artwork\\' + album +'.jpg')		
    if q == number_items: 
            renameoutputfolder(playlistname)
ydl_opts = {
    'outtmpl' : '/' + '%(default)s' + '/%(default)s.%(ext)s', 'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }], 'output':'video'
}

def setfilename(back, lead):
    global check, q
    collect = lead + " - " + back         
    check.append(collect)
    q+=1
    filename = collect +'.mp3'
    return filename
 	

def renameoutputfolder(playlistname):
	output_folder = os.getcwd()
	os.rename(output_folder+"/NA", output_folder+"/"+playlistname)
