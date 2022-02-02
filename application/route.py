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
