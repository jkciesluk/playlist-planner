import unittest
import json
import random  
import string

from application.mymap import MyMap
from application.models import User
from application.project import PlaylistForRoute  
from application.route import Route
from application.spotify import Spotify

with open('application/testdata/mockroute.json', 'r') as f:
    routeData = json.load(f)["resourceSets"][0]["resources"][0]
with open('application/testdata/mocksongs.json', 'r') as f:
    songsData = json.load(f)
  
myMap = MyMap()
totalDistance = myMap.getTotalDistance(routeData)
totalDuration = myMap.getTotalDuration(routeData)
itineraryPoints = myMap.getItineraryPoints(routeData)
  
class RouteTest(unittest.TestCase):
        
  def test_intervalPointsDuration(self):
    route = Route({"travelDistance": totalDistance, "travelDuration": totalDuration, "itineraryPoints": itineraryPoints})
    travelDuration = routeData['travelDuration']
    intervalPoints = route.intervalPoints()
    self.assertAlmostEqual(travelDuration, intervalPoints[-1]['travelDuration'], msg="Interval points don't sum up to correct travel duration")
  
  def test_intervalPointsDistance(self):
    route = Route({"travelDistance": totalDistance, "travelDuration": totalDuration, "itineraryPoints": itineraryPoints})
    travelDistance = routeData['travelDistance']
    intervalPoints = route.intervalPoints()
    self.assertAlmostEqual(travelDistance, intervalPoints[-1]['travelDistance'], msg="Interval points don't sum up to correct travel distance")


class UserTest(unittest.TestCase):
  def test_password(self):
    base = string.ascii_letters + string.digits
    length = random.randint(1, 30)
    randomPassword = ''.join(random.choice(base) for i in range(length))
    user = User()
    user.set_password(randomPassword)
    self.assertTrue(user.check_password(randomPassword), "Saving password doesn't work")


class PlaylistForRouteTest(unittest.TestCase):
  mockSpitifyClient = Spotify("1234567890")
  playlist = PlaylistForRoute(Route({"travelDistance": totalDistance, "travelDuration": totalDuration, "itineraryPoints": itineraryPoints}  ), 
                                mockSpitifyClient,
                                'Golczewo',
                                'Wrocław')
    
  def test_correctLength(self):
    playlist = PlaylistForRouteTest.playlist
    zipped = playlist.zipSongsWithTime(songsData)
    self.assertGreaterEqual(zipped[-1]['timeCovered'], playlist.route.totalDuration)
  
  def test_maneuverPoints(self):
    playlist = PlaylistForRouteTest.playlist
    songsOnManeuvers = playlist.songsOnManeuvers(playlist.zipSongsWithTime(songsData))['items']
    self.assertEqual(len(playlist.route.intervalPoints()), len(songsOnManeuvers), "Amount of maneuvers not equal amount of itinerary points")

if __name__ == "__main__":
    unittest.main()
