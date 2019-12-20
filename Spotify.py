import spotipy
import spotipy.util as util
import pickle
import json
import time
import logging
import threading
import pprint

from difflib import SequenceMatcher
from random import randint


# string similarity
def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()


class SpotifyAgent:


    def __init__(self):
        scope = 'user-library-read user-modify-playback-state user-read-playback-state playlist-modify-public playlist-modify-private'
        token = util.prompt_for_user_token('Vaibhav Bafna', scope,client_id='d6f3df49b6634cbb94e820d337fda4e2',client_secret='3280007444f04aada6de9cc3639beb0e',redirect_uri='http://localhost/')
        self.client = spotipy.Spotify(auth=token)
        self.state = {
            'playing': False
        }
        self.playlist_thread = None
        self.stop_threads = False

        print("Spotify client booted successfully")


    def get_active_device_id(self):
        devices = self.client.devices()['devices']
        device_id = ""

        for device in devices: 
            if device['is_active'] == True:
                device_id = device['id']
                break

        return device_id


    def pause(self):
        device_id = self.get_active_device_id()
        self.client.pause_playback(device_id=device_id)
        self.state['playing'] = False


    def play(self):
        self.shuffle()
        device_id = self.get_active_device_id()
        self.client.start_playback(device_id=device_id)
        self.state['playing'] = True


    def play_playlist(self, playlist_name):
        available_playlists = self.client.current_user_playlists()
        final_playlist = ""
        final_playlist_id = ""
        final_playlist_uri = ""

        # find the most similar playlist to the one user mentioned
        max_similarity_score = -1
        for item in available_playlists['items']:
            current_similarity_score = similar(playlist_name, item['name'])
            if max_similarity_score < current_similarity_score:
                max_similarity_score = current_similarity_score
                final_playlist = item['name']
                final_playlist_id = item['id']
                final_playlist_uri = item['uri']

        # fallback in case no playlist is found
        if final_playlist == "":
            return False
        else:
            self.shuffle()
            self.client.start_playback(context_uri=final_playlist_uri)
            return True


    def play_artist(self, artist):

        artist_search_results = self.client.search(q=artist, type='artist')

        final_artist = ""
        final_artist_uri = ""

        # find the most similar artist to the one the user mentioned
        max_similarity_score = -1
        for artist_item in artist_search_results['artists']['items']:
            current_similarity_score = similar(artist, artist_item['name'])
            if max_similarity_score < current_similarity_score:
                max_similarity_score = current_similarity_score
                final_artist = artist_item['name']
                final_artist_uri = artist_item['uri']

        if final_artist == "":
            return False
        else:
            # self.shuffle()
            self.client.start_playback(context_uri=final_artist_uri)
            return True


    def get_current_playlists(self):
        available_playlists = self.client.current_user_playlists()
        return available_playlists['items']


    def shuffle(self):
        shuffle = randint(0, 1)
        if shuffle == 0:
            self.client.shuffle(False)
        else:
            self.client.shuffle(True)


    def record_spotify_session(self):

        # name playlist
        import datetime
        today = datetime.date.today()
        playlist_name = "sandbox session: " + today.strftime('%d-%b-%Y')

        # create playlist
        user_id = self.client.me()['id']
        playlist_data = self.client.user_playlist_create(user_id, playlist_name)
        playlist_id = playlist_data['id']

        print("playlist successfully created")
        pprint.pprint(playlist_data)

        # start thread for recording playlists here
        x = threading.Thread(target=self.helper_record_spotify_session, args=(playlist_id,), daemon=True)
        self.playlist_thread = x
        print("playlist thread has been started")
        x.start()


    def stop_recording_spotify_session(self):
        print("about to kill spotify thread")
        self.stop_threads = True
        self.playlist_thread.join()
        print("thread has been killed")


    # use this function as a thread
    def helper_record_spotify_session(self, playlist_id):
        print("hello, your spotify thread is alive and well ", playlist_id)
        self.stop_threads = False
        time.sleep(2)

        curr_track = self.client.current_user_playing_track()
        print("curr_track: ", curr_track)

        # if music is not on, wait a full minute before adding to playlist
        TIMEOUT = 60
        if (curr_track == None):
            time.sleep(TIMEOUT)

        user_id = self.client.me()['id']    

        cached_track = ''
        while (True):

            curr_track = self.client.current_user_playing_track()['item']['uri']

            if curr_track == None or self.stop_threads:
                break
            else:
                if cached_track != curr_track:
                    tracks = []
                    tracks.append(curr_track)
                    self.client.user_playlist_add_tracks(user_id, playlist_id, tracks)
                    cached_track = curr_track
                
                time.sleep(TIMEOUT)