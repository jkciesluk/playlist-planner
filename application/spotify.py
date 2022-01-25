import requests
import json

class Spotify():
  def __init__(self, access_token):
      self.access_token = access_token
      self.user_id = None
      self.getCurrentUser()
  
  def getCurrentUser(self):
    headers = {'Authorization': f'Bearer {self.access_token}',
               'Content-Type': 'application/json'}
    r = requests.get("https://api.spotify.com/v1/me", headers=headers)
    self.id = r.json()['id']
  
  def getTopItems(self, type, limit, time_range,offset=0):
    params = {
      "limit": limit,
      "offset": offset,
      "time_range": time_range
    }
    headers = {'Authorization': f'Bearer {self.access_token}',
               'Content-Type': 'application/json'}
    r = requests.get(f"https://api.spotify.com/v1/me/top/{type}", params=params, headers=headers)
    return r.json
  
  def createPlaylist(self, name, description=""):
    headers = {'Authorization': f'Bearer {self.access_token}',
               'Content-Type': 'application/json'}
    data={
      "name": name,
      "description": description,
    }
    r = requests.post(f"https://api.spotify.com/v1/users/{self.user_id}/playlists", data=json.dumps(data), headers=headers)
    return r.status_code

  def addItemsToPlaylist(self, playlist_id, uris):
    headers = {'Authorization': f'Bearer {self.access_token}',
               'Content-Type': 'application/json'}
    data = {"uris": uris}
    r = requests.post(f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks", headers=headers, data=json.dumps(data))
  
