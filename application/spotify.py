import requests
import json


class Spotify():
    def __init__(self, access_token):
        self.access_token = access_token
        self.user_id = None
        self.getCurrentUser()

    # set user_id for currently authorized user
    def getCurrentUser(self):
        headers = {'Authorization': f'Bearer {self.access_token}',
                   'Content-Type': 'application/json'}
        r = requests.get("https://api.spotify.com/v1/me", headers=headers)
        if 'id' in r.json():
          self.user_id = r.json()['id']

    # get user top items from time_range
    def getTopItems(self, type, limit, time_range, offset=0):
        params = {
            "limit": limit,
            "offset": offset,
            "time_range": time_range
        }
        headers = {'Authorization': f'Bearer {self.access_token}',
                   'Content-Type': 'application/json'}
        r = requests.get(
            f"https://api.spotify.com/v1/me/top/{type}", params=params, headers=headers)

        return r.json()['items']

    # get user top songs
    def getTopSongs(self, amount, time_range, offset=0):
        return self.stripSongs(self.getTopItems("tracks", amount, time_range, offset))

    # get user top artists
    def getTopArtists(self, amount, time_range, offset=0):
        return self.stripArtists(self.getTopItems("artists", amount, time_range, offset))

    # map songs
    def stripSongs(self, songs):
        return list(map(lambda song: {
            'spotify_uri': song['uri'],
            'spotify_id': song['id'],
            'duration': song['duration_ms']/1000,
            'name': song['name'],
            'artists': self.stripArtists(song['artists'])
        }, songs))

    # map artists
    def stripArtists(self, artists):
        return list(map(lambda artist: {
            'name': artist['name'],
            'spotify_id': artist['id'],
            'spotify_uri': artist['uri'],
        }, artists))

    # create playlist with name and description
    def createPlaylist(self, name, description=""):
        headers = {'Authorization': f'Bearer {self.access_token}',
                   'Content-Type': 'application/json'}
        data = {
            "name": name,
            "description": description,
        }
        r = requests.post(
            f"https://api.spotify.com/v1/users/{self.user_id}/playlists", data=json.dumps(data), headers=headers)
        return r.json()['id']

    # add tracks to playlist
    def addItemsToPlaylist(self, playlist_id, uris):
        headers = {'Authorization': f'Bearer {self.access_token}',
                   'Content-Type': 'application/json'}
        data = {"uris": uris}
        r = requests.post(
            f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks", headers=headers, data=json.dumps(data))
        return 0
