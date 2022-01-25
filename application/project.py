import requests

class MyMap:
  __key = "AsteIyPnZzvNB9aYKbrhImkSd7kFdJ-GZOz4GawrO6qssxqBMGW5z0Ks-xSm3A6s"
      
  def __getItineraryPoints(self, route):
    itinerary = route["routeLegs"][0]["itineraryItems"]
    itineraryItems = list(map(lambda item: {"intervalDistance": item["travelDistance"], "intervalDuration": item["travelDuration"], "coords": item["maneuverPoint"]["coordinates"]}, itinerary))
    return itineraryItems[::-1]

  def __getTotalDistance(self, route):
    return route["travelDistance"]
      
  def __getTotalDuration(self, route):
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
    totalDistance = self.__getTotalDistance(route)
    totalDuration = self.__getTotalDuration(route)
    itineraryPoints = self.__getItineraryPoints(route)
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
      intervals.append({"travelDistance": distance, "travelDuration": duration, "coords": point["coords"]})
    return intervals



#SpotifyHandler()
#mapa = MyMap()
#route = mapa.getRouteData("Golczewo", "Golanice")
#print(route.intervalPoints())