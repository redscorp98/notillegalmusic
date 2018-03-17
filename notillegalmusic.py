import spotipy, requests
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.util import prompt_for_user_token

import Downloader
class NotIllegal:
    def __init__(self, username, spotify):
        self.username = username
        self.location = ["User", username]
        self.spotify = spotify
        self.playlists = self.spotify.user_playlists(username)
        self.commands = {"dir": self.show_playlists,
                "cd": self.show_contents,
                "dl": self.download}
        self.selection = -1

    def mainloop(self):
        running = True
        while running:
            loc = "s:"
            for i in range(len(self.location)):
                loc += "\\"+self.location[i]
            print(loc+">", end="")
            user = input()
            running = self.run(user)
            print()

    def run(self, cmd):
        running = True
        user = cmd.split()
        length = len(user)
        if not length:
            pass
        elif user[0] in ["quit", "q"]:
            running = False
        elif length == 1:
            self.commands[user[0]]()
        elif length == 2:
            try:
                self.commands[user[0]](int(user[1]))
            except ValueError:
                self.commands[user[0]](user[1])
        else:
            pass
        return running

    def setLocation(self, location):
        self.location = location

    def getLocation(self):
        return self.location

    def setUsername(self, username):
        self.username = username

    def getUsername(self):
        return self.username

    def show_tracks(self, results, offset):
        for i, item in enumerate(results['items']):
            track = item['track']
            print("   %d %32.32s %s" % (i + 1 + 100*offset, track['artists'][0]['name'], track['name']))

    def show_playlists(self):
        playlists = self.playlists
        hasNext = True
        while hasNext:
            for i, playlist in enumerate(playlists['items']):
                if i % 2:
                    print("%4d %32.32s" % (i + 1 + playlists['offset'], playlist['name']))
                else:
                    print("%4d %32.32s" % (i + 1 + playlists['offset'], playlist['name']), end="\t")
            if playlists['next']:
                playlists = self.spotify.next(playlists)
            else:
                hasNext = False

    def show_contents(self, select='.'):
        playlists = self.playlists
        selection = 0
        location = self.location
        if select == ".":
            if len(location) == 2:
                self.sign_out()
            elif len(location) == 3:
                self.location.pop(2)
            else:
                return
        for playlist in playlists['items']:
            selection += 1
            if selection == select:
                print()
                print(playlist['name'])
                self.setLocation(location+[playlist['name']])
                print(' total tracks', playlist['tracks']['total'])
                results = self.spotify.user_playlist(self.username, playlist['id'], fields="tracks,next")
                tracks = results['tracks']
                self.show_tracks(tracks, 0)
                offset = 0
                while tracks['next']:
                    tracks = self.spotify.next(tracks)
                    self.show_tracks(tracks, offset)
                    offset += 1
                self.selection = selection
                return

    def download(self):
        playlists = self.playlists
        count = 1
        for playlist in playlists['items']:
            if count == self.selection:
                print("downloading " + '"'+ playlist['name']+'"')
                #print(' total tracks', playlist['tracks']['total'])
                results = self.spotify.user_playlist(self.getUsername(), playlist['id'], fields="tracks,next")
                tracks = results['tracks']
                for i, item in enumerate(tracks['items']):
                    track = item['track']
                    album = track['album']
                    Downloader.download(track['artists'][0]['name'], track['name'], track['track_number'], track['artists'][0]['name'], album['name'], playlist['name'])
                return
            else:
                count += 1

    def sign_out(self):
        location = self.location
        global running
        location.pop(0)
        username = input("Username: ")
        if username not in ["quit", "q"]:
            prompt_for_user_token(username, 'playlist-read-private', client_id=CLIENT_ID, client_secret=CLIENT_SECRET,
                                  redirect_uri=CALLBACK)
            self.setUsername(username)
            self.playlists = self.spotify.user_playlists(username)
            location.append(username)
        else:
            running = False
        self.location = location

def main():
    CLIENT_SECRET = "e71f42f12c0d47cb8c4d694033e016e8"
    CLIENT_ID = "184a3e47b6c44f828a5bdfdbedb2fa14"
    CALLBACK = "http://localhost/callback"
    username = "MrPerfectFace" #input("Username: ")
    prompt_for_user_token(username, 'playlist-read-private', client_id=CLIENT_ID, client_secret=CLIENT_SECRET,
                          redirect_uri=CALLBACK)
    client_credentials_manager = SpotifyClientCredentials(CLIENT_ID, CLIENT_SECRET)
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
    notillegal = NotIllegal(username, sp)
    notillegal.mainloop()

if __name__ == '__main__':
    main()
