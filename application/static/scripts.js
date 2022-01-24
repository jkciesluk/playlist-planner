
/*
 * Directions
 * https://docs.microsoft.com/en-us/bingmaps/v8-web-control/map-control-concepts/directions-module-examples/?toc=https%3A%2F%2Fdocs.microsoft.com%2Fen-us%2Fbingmaps%2Fv8-web-control%2Ftoc.json&bc=https%3A%2F%2Fdocs.microsoft.com%2Fen-us%2FBingMaps%2Fbreadcrumb%2Ftoc.json
 *
*/

function GetMap() {
    var map = new Microsoft.Maps.Map('#myMap', {
        credentials: 'AsteIyPnZzvNB9aYKbrhImkSd7kFdJ-GZOz4GawrO6qssxqBMGW5z0Ks-xSm3A6s',
        center: new Microsoft.Maps.Location(53.826111, 14.981944)
    });
    
    Microsoft.Maps.loadModule('Microsoft.Maps.Directions', function () {
        
        var directionsManager = new Microsoft.Maps.Directions.DirectionsManager(map);
        directionsManager.setRequestOptions({ routeMode: Microsoft.Maps.Directions.RouteMode.driving });
        const start = Microsoft.Maps.Directions.Waypoint({address: "Golczewo"})
        const end = Microsoft.Maps.Directions.Waypoint({address: "Wolin"})
        directionsManager.addWaypoint(start)
        directionsManager.addWaypoint(end)

        Microsoft.Maps.Events.addHandler(directionsManager, 'directionsError', directionsError);
        Microsoft.Maps.Events.addHandler(directionsManager, 'directionsUpdated', directionsUpdated);
        
        //Calculate directions.
        directionsManager.calculateDirections();
    });
}

function directionsUpdated(e) {
  //Get the current route index.
  var routeIdx = directionsManager.getRequestOptions().routeIndex;

  //Get the distance of the route, rounded to 2 decimal places.
  var distance = Math.round(e.routeSummary[routeIdx].distance * 100)/100;

  //Get the distance units used to calculate the route.
  var units = directionsManager.getRequestOptions().distanceUnit;
  var distanceUnits = '';

  if (units == Microsoft.Maps.Directions.DistanceUnit.km) {
      distanceUnits = 'km'
  } else {
      //Must be in miles
      distanceUnits = 'miles'
  }

  //Time is in seconds, convert to minutes and round off.
  var time = Math.round(e.routeSummary[routeIdx].timeWithTraffic / 60);

  document.getElementById('routeInfoPanel').innerHTML = 'Distance: ' + distance + ' ' + distanceUnits + '<br/>Time with Traffic: ' + time + ' minutes';
}

function directionsError(e) {
  alert('Error: ' + e.message + '\r\nResponse Code: ' + e.responseCode)
}

const form = document.getElementById('myform');
const start = document.getElementById('startForm');
const Destination = document.getElementById("destForm");

form.addEventListener("submit", (event) => {
    
  //TODO:
  //Na submicie wyslij request do serwera z danymi
  //nastepnie stwórz pushpiny itd
  if (valid()) {
      alert('Incorrect input!');
      event.preventDefault();
  }
  else return true;
});
