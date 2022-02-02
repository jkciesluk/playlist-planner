from .spotify import Spotify
from .route import Route
import random


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
