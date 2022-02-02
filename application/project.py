import requests
from .spotify import Spotify
import random


class MyMap:
    __key = "AsteIyPnZzvNB9aYKbrhImkSd7kFdJ-GZOz4GawrO6qssxqBMGW5z0Ks-xSm3A6s"

    # get itinerarty points from route
    def getItineraryPoints(self, route):
        itinerary = route["routeLegs"][0]["itineraryItems"]
        itineraryItems = list(map(lambda item: {
            "intervalDistance": item["travelDistance"],
            "intervalDuration": item["travelDuration"],
            "coords": item["maneuverPoint"]["coordinates"],
            'maneuver': item['instruction']['text']}, itinerary))
        return itineraryItems

    # get route distance
    def getTotalDistance(self, route):
        return route["travelDistance"]

    # get route duration
    def getTotalDuration(self, route):
        return route["travelDuration"]

    # send request to microsoft maps api for route
    def getRoute(self, start, end, type="Driving"):
        url = f"http://dev.virtualearth.net/REST/V1/Routes/{type}?wp.1={start}&wp.2={end}&distanceUnit=km&key={self.__key}"
        r = requests.get(url)
        if(r.status_code != 200):
            print("Error!")
            raise Exception
        else:
            jsonRoute = r.json()
            return jsonRoute["resourceSets"][0]["resources"][0]

    # get route from start to end
    def getRouteData(self, start, end, type):
        route = self.getRoute(start, end, type)
        totalDistance = self.getTotalDistance(route)
        totalDuration = self.getTotalDuration(route)
        itineraryPoints = self.getItineraryPoints(route)
        return Route({"travelDistance": totalDistance, "travelDuration": totalDuration, "itineraryPoints": itineraryPoints})


class Route:

    def __init__(self, route):
        self.route = route
        self.itineraryPoints = route["itineraryPoints"]
        self.totalDistance = route["travelDistance"]
        self.totalDuration = route["travelDuration"]

    # map interval points
    def intervalPoints(self):
        distance = 0
        duration = 0
        intervals = []
        for point in self.itineraryPoints:
            distance += point["intervalDistance"]
            duration += point["intervalDuration"]
            intervals.append({"travelDistance": distance,
                              "travelDuration": duration,
                              "lat": point["coords"][0],
                              'long': point['coords'][1],
                              'maneuver': point['maneuver']})
        return intervals


class PlaylistForRoute():
    def __init__(self, route: Route, spotifyClient: Spotify, start, end):
        self.start = start
        self.end = end
        self.route = route
        self.spotifyClient = spotifyClient
        self.length = route.totalDuration

    # calculate needed songs
    def songsForRoute(self, time_range):
        timeCovered = 0.0
        j = 0
        result = []
        while(timeCovered < self.length):
            i = 0
            tracks = self.spotifyClient.getTopSongs(40, time_range, 40*j)
            while (timeCovered < self.length and i < len(tracks)):
                timeCovered += tracks[i]['duration']
                result.append(tracks[i])
                i += 1
            j += 1
        random.shuffle(result)
        return result

    # zip songs with covered time
    def zipSongsWithTime(self, songs):
        timeCovered = 0.0
        zipped = []
        for song in songs:
            timeCovered += song['duration']
            zipped.append({'timeCovered': timeCovered, 'song': song})
        return zipped

    # calculate which song will be playing on maneuver
    def songsOnManeuvers(self, zipped):
        maneuvers = self.route.intervalPoints()
        i = 0
        result = []
        for point in maneuvers:
            while(zipped[i]['timeCovered'] < point['travelDuration']):
                i += 1
            result.append({'lat': point['lat'],
                           'long': point['long'],
                           'maneuver': point['maneuver'],
                           'song': zipped[i]['song']['name'],
                           'artists': list(map(lambda artist: artist['name'], zipped[i]['song']['artists']))})
        return {'items': result}

    # create playlist, time_range defines where to look for songs
    def createPlaylistForRoute(self, time_range):
        name = f'{self.start} - {self.end}'
        description = f'Playlist for trip from {self.start} to {self.end}'
        playlist = self.spotifyClient.createPlaylist(name, description)
        songs = self.songsForRoute(time_range)
        uris = list(map(lambda song: song['spotify_uri'], songs))
        res = self.spotifyClient.addItemsToPlaylist(playlist, uris)
        return self.songsOnManeuvers(self.zipSongsWithTime(songs))
