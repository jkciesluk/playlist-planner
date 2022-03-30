import requests
from .route import Route

class MyMap:
    # Insert your app key here
    __key = ""

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
