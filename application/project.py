import requests
from .spotify import Spotify

class MyMap:
  __key = "AsteIyPnZzvNB9aYKbrhImkSd7kFdJ-GZOz4GawrO6qssxqBMGW5z0Ks-xSm3A6s"
      
  def getItineraryPoints(self, route):
    itinerary = route["routeLegs"][0]["itineraryItems"]
    itineraryItems = list(map(lambda item: {
      "intervalDistance": item["travelDistance"], 
      "intervalDuration": item["travelDuration"], 
      "coords": item["maneuverPoint"]["coordinates"], 
      'maneuver': item['instruction']['text']}
      ,itinerary))
    return itineraryItems

  def getTotalDistance(self, route):
    return route["travelDistance"]
      
  def getTotalDuration(self, route):
    return route["travelDuration"]
  
  def getRoute(self, start, end, type="Driving"):
    url = f"http://dev.virtualearth.net/REST/V1/Routes/{type}?wp.1={start}&wp.2={end}&distanceUnit=km&key={self.__key}"
    r = requests.get(url)
    if(r.status_code != 200):
      print("Error!")
      raise Exception
    else:
      jsonRoute = r.json()
      return jsonRoute["resourceSets"][0]["resources"][0]
  
  def getRouteData(self, start, end):
    route = self.getRoute(start, end)
    totalDistance = self.getTotalDistance(route)
    totalDuration = self.getTotalDuration(route)
    itineraryPoints = self.getItineraryPoints(route)
    return Route({"travelDistance": totalDistance, "travelDuration": totalDuration, "itineraryPoints": itineraryPoints})


class Route:
  
  def __init__(self, route):
    self.route = route
    self.itineraryPoints = route["itineraryPoints"]    
    self.totalDistance = route["travelDistance"]    
    self.TotalDuration = route["travelDuration"]    

  def intervalPoints(self):
    distance = 0
    duration = 0
    intervals = []
    for point in self.itineraryPoints:
      distance += point["intervalDistance"]
      duration += point["intervalDuration"]
      intervals.append({"travelDistance": distance, "travelDuration": duration, "coords": point["coords"], 'maneuver': point['maneuver']})
    return intervals


class PlaylistForRoute():
  def __init__(self, route: Route, spotifyClient: Spotify, start, end):
    self.start = start
    self.end = end
    self.route = route
    self.spotifyClient = spotifyClient     
    self.length = route.totalDuration
  
  def songsForRoute(self):
    tracks = self.spotifyClient.getTopSongs(40)
    timeCovered = 0.0
    i = 0
    while (timeCovered < self.length):
      timeCovered += tracks[i]['duration']
      i += 1
    return tracks[:i]

  def zipSongsWithTime(self, songs):
    timeCovered = 0.0
    zipped = []
    for song in songs:
      timeCovered += song['duration']
      zipped.append((timeCovered, song))
    return zipped

  def songsOnManeuvers(self, zipped):
    maneuvers = self.route.intervalPoints()
    i = 0
    result = []
    for point in maneuvers:
      while(zipped[i][0] < point['travelDuration']):
        i += 1
      result.append((point, zipped[i][1]))
    return result

  def createPlaylistForRoute(self):
    name = f'{self.route.start} - {self.route.end}'
    description = f'Playlist for trip from {self.route.start} to {self.route.end}'
    playlist = self.spotifyClient.createPlaylist(name, description)
    songs = self.songsForRoute()
    uris = list(map(lambda song: song['spotify_uri'], songs))
    self.spotifyClient.addItemsToPlaylist(playlist, uris)
    return self.songsOnManeuvers(self.zipSongsWithTime(songs))


  
#SpotifyHandler()
#mapa = MyMap()
#route = mapa.getRouteData("Golczewo", "Golanice")
#print(route.intervalPoints())