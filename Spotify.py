import spotipy
import spotipy.util as util

class SpotifyAgent:

    def __init__(self):
        scope = 'user-library-read user-modify-playback-state user-read-playback-state'
        token = util.prompt_for_user_token('Vaibhav Bafna', scope,client_id='d6f3df49b6634cbb94e820d337fda4e2',client_secret='3280007444f04aada6de9cc3639beb0e',redirect_uri='http://localhost/')
        self.client = spotipy.Spotify(auth=token)
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

    def play(self):
        device_id = self.get_active_device_id()
        self.client.start_playback(device_id=device_id)
