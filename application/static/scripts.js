function GetMap() {
  const points = {}
  const map = new Microsoft.Maps.Map('#myMap', {
      credentials: 'AsteIyPnZzvNB9aYKbrhImkSd7kFdJ-GZOz4GawrO6qssxqBMGW5z0Ks-xSm3A6s',
  });

  const infobox = new Microsoft.Maps.Infobox(map.getCenter(), {
    visible: false
  });
  
  infobox.setMap(map);

  Microsoft.Maps.loadModule('Microsoft.Maps.Directions', function () {
        
    var directionsManager = new Microsoft.Maps.Directions.DirectionsManager(map);
    directionsManager.setRequestOptions({ routeMode: Microsoft.Maps.Directions.RouteMode.driving });
    const start = Microsoft.Maps.Directions.Waypoint({address: "Golczewo"})
    const end = Microsoft.Maps.Directions.Waypoint({address: "Wolin"})
    directionsManager.addWaypoint(start)
    directionsManager.addWaypoint(end)

    //Calculate directions.
    directionsManager.calculateDirections();
  });

  }
