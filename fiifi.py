import spotipy, requests
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.util import prompt_for_user_token

import Downloader
global location
global name
global sp

def show_tracks(results, offset):
    for i, item in enumerate(results['items']):
        track = item['track']
        print("   %d %32.32s %s" % (i + 1 + 100*offset, track['artists'][0]['name'], track['name']))

def show_playlists(playlists):
    chocolate = True
    while chocolate:
        for i, playlist in enumerate(playlists['items']):
            if i % 2:
                print("%4d %32.32s" % (i + 1 + playlists['offset'], playlist['name']))
            else:
                print("%4d %32.32s" % (i + 1 + playlists['offset'], playlist['name']), end="\t")
        if playlists['next']:
            playlists = sp.next(playlists)
        else:
            chocolate = False

def show_contents(playlists, select):
    global location
    global sp
    global pl
    pl = 0
    if select == ".":
        if len(location) == 2:
            sign_out()
        elif len(location) == 3:
            location.pop(2)
        else:
            return
    for playlist in playlists['items']:
        pl += 1
        if pl == select:
            print()
            print(playlist['name'])
            location += [playlist['name']]
            print(' total tracks', playlist['tracks']['total'])
            results = sp.user_playlist(username, playlist['id'], fields="tracks,next")
            tracks = results['tracks']
            show_tracks(tracks, 0)
            offset = 0
            while tracks['next']:
                tracks = sp.next(tracks)
                show_tracks(tracks, offset)
                offset += 1

def download(playlists):
    global sp
    global pl
    count = 1
    for playlist in playlists['items']:
        if count == pl:
            print("downloading " + '"'+ playlist['name']+'"')
            #print(' total tracks', playlist['tracks']['total'])
            results = sp.user_playlist(username, playlist['id'], fields="tracks,next")
            tracks = results['tracks']
            #tracks = sp.next(tracks)
            for i, item in enumerate(tracks['items']):
                track = item['track']
                Downloader.download(track['artists'][0]['name'], track['name'], i+1, "Various Artists", playlist['name'])
        else:
            count += 1

def sign_out():
    global location
    global username
    global running
    location.pop(0)
    username = input("Username: ")
    if username not in ["quit", "q"]:
        prompt_for_user_token(username, 'playlist-read-private', client_id=CLIENT_ID, client_secret=CLIENT_SECRET,
                              redirect_uri=CALLBACK)
        playlists = sp.user_playlists(username)
        location.append(username)
    else:
        running = False

CLIENT_SECRET = "e71f42f12c0d47cb8c4d694033e016e8"
CLIENT_ID = "184a3e47b6c44f828a5bdfdbedb2fa14"
CALLBACK = "http://localhost/callback"

#playlists = sp.user_playlists(username)

def main():
    global location
    global username
    global sp
    username = input("Username: ")
    prompt_for_user_token(username, 'playlist-read-private', client_id=CLIENT_ID, client_secret=CLIENT_SECRET,
                          redirect_uri=CALLBACK)
    client_credentials_manager = SpotifyClientCredentials(CLIENT_ID, CLIENT_SECRET)
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
    playlists = sp.user_playlists(username)
    location = ["User", username]
    running = True
    commands = {"dir": show_playlists,
                "cd": show_contents,
                "dl": download}
    while running:
        for i in range(len(location)):
            print("\\"+location[i], end="")
        print(">", end="")
        user = input()
        user = user.split()
        length = len(user)
        if not length:
            pass
        elif user[0] in ["quit", "q"]:
            running = False
        elif length == 1:
            commands[user[0]](playlists)
        elif length == 2:
            try:
                commands[user[0]](playlists, int(user[1]))
            except ValueError:
                commands[user[0]](playlists, user[1])
        else:
            pass
        print()

if __name__ == '__main__':
    main()
