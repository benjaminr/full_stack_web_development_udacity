////////////////////////////////////////////////////////////////////////////////
// GLOBALS
////////////////////////////////////////////////////////////////////////////////
// Maps Markers
var markers = ko.observableArray([]);
// Filter for cards and markers
var currentFilter = ko.observable();
// Global for Google map
var map;
// SONGKICK API Key
var api_key = "";
// SONGKICK Locations Endpoint
var locations_rest_endpoint = `https://api.songkick.com/api/3.0/search/locations.json?location=geo`;
var infowindow;
////////////////////////////////////////////////////////////////////////////////

////////////////////////////////////////////////////////////////////////////////
// knockoutjs MVVM
////////////////////////////////////////////////////////////////////////////////
function EventsViewModel() {

    var self = this;

    // Enable filtering of markers
    self.filterMarkers = ko.computed(function() {
      if(!currentFilter()) {
          return markers();
      } else if (currentFilter() == "All") {
          return markers().filter(function(marker) {
              marker.setVisible(true);
              return true;
          });
      }
      else {
          return markers().filter(function(marker) {
              if (marker.type != currentFilter()) {
                marker.setVisible(false);
              } else {
                marker.setVisible(true);
                return true;
              }
          });
      }
    }, this);

    self.filter = function (type) {
        currentFilter(type);
    };

    self.showMarker = function(id) {
        return markers().filter(function(marker) {
          if (marker.id == id) {
              marker.setVisible(true);
              marker.setAnimation(google.maps.Animation.BOUNCE);
              setTimeout(function(){ marker.setAnimation(null); }, 750);
              map.setCenter(marker.getPosition());
              infowindow.setContent(marker.content);
              infowindow.open(map, marker);
          } else {
              marker.setVisible(false);
          }
        });
    };

}
////////////////////////////////////////////////////////////////////////////////
function googleMapsError(data) {
  alert("Map API Failed");
}
////////////////////////////////////////////////////////////////////////////////
// Helper Functions
////////////////////////////////////////////////////////////////////////////////
function createMarker(place, delay_time) {

    // Store the venue coordinates as local vars
    var lat = place.venue.lat;
    var lng = place.venue.lng;

    // Venue information HTML for Google maps infowindow
    var content = '<p><a href="' + place.uri + '">' + place.displayName + '</a>' + '</p>';

    // Create a marker and add additional params from SONGKICK data
    var marker = new google.maps.Marker({
      map: map,
      animation: google.maps.Animation.DROP,
      position: {lat: lat, lng: lng},
      id: place.id,
      type: place.type,
      uri: place.uri,
      venue: place.venue,
      location: place.location,
      artist: place.performance[0].artist,
      date: place.start.date,
      popularity: place.popularity,
      content: content
    });

    // Place marker into markers Knockoutjs observableArray
    markers.push(marker);

    // Create listener for users clicking for info
    google.maps.event.addListener(marker, 'click', function() {
      infowindow.setContent(content);
      infowindow.open(map, this);
      marker.setAnimation(google.maps.Animation.BOUNCE);
      setTimeout(function(){ marker.setAnimation(null); }, 750);
    });
}
////////////////////////////////////////////////////////////////////////////////
function setVisibleOnAll(value) {
  markers().forEach(function(v,i){
    v.setVisible(value);
  });
}
////////////////////////////////////////////////////////////////////////////////
function createMarkers(events) {
  var delay_time = 1;
  events.forEach(function(event) {
    createMarker(event, delay_time);
    delay_time += 5;
  });
}
////////////////////////////////////////////////////////////////////////////////
function getSongkickEventsLocation(lat, lng) {
  $.getJSON(locations_rest_endpoint + `:${lat},${lng}&apikey=${api_key}`, function(data) {
    var metro_area_id = data.resultsPage.results.location[0].metroArea.id;
    var upcomingEvents = `https://api.songkick.com/api/3.0/metro_areas/${metro_area_id}/calendar.json?apikey=${self.api_key}`;
    $.getJSON(upcomingEvents, function(data) {
      var events = data.resultsPage.results.event;
      console.log(events);
      createMarkers(events);
    })
    .fail(function(data){
        alert("Event Search Failed");
    });
  })
  .fail(function(data){
      alert("Venue Search Failed");
  });
}
////////////////////////////////////////////////////////////////////////////////
// Google Maps
////////////////////////////////////////////////////////////////////////////////
function initMap() {
  map = new google.maps.Map(document.getElementById('map'), {
    center: {
      lat: 51.50,
      lng: 0.12
    },
    zoom: 8
  });

  // Grab DOM elements for card and user input, assign local vars
  var card = document.getElementById('maps-card');
  var input = document.getElementById('maps-input');

  map.controls[google.maps.ControlPosition.TOP_RIGHT].push(card);

  var autocomplete = new google.maps.places.Autocomplete(input);

  autocomplete.setOptions({
    strictBounds: this.checked
  });

  // Bind the map's bounds (viewport) property to the autocomplete object,
  // so that the autocomplete requests use the current map bounds for the
  // bounds option in the request.
  autocomplete.bindTo('bounds', map);

  infowindow = new google.maps.InfoWindow();

  getSongkickEventsLocation(51.50, 0.12);

  // When a user types a new location
  autocomplete.addListener('place_changed', function() {
    infowindow.close();

    var marker = new google.maps.Marker({
      map: null,
      anchorPoint: new google.maps.Point(0, -29)
    });

    var place = autocomplete.getPlace();
    if (!place.geometry) {
      // User entered the name of a Place that was not suggested and
      // pressed the Enter key, or the Place Details request failed.
      window.alert("No details available for input: '" + place.name + "'");
      return;
    }

    // If the place has a geometry, then present it on a map.
    if (place.geometry.viewport) {
      map.fitBounds(place.geometry.viewport);
      map.setZoom(8);
    } else {
      map.setCenter(place.geometry.location);
      map.setZoom(8);
    }

    // Set lat lng for shorthand
    lat = place.geometry.location.lat();
    lng = place.geometry.location.lng();

    // Set marker props
    marker.setPosition(place.geometry.location);
    marker.setVisible(true);

    // Clear Existing markers
    setVisibleOnAll(false);
    markers.removeAll();

    // Get new data and create markers
    getSongkickEventsLocation(lat, lng);

    // Sort by popularity
    markers.sort(function(a, b) {
      return a.popularity - b.popularity;
    });
    markers.reverse();
  });
}

ko.applyBindings(EventsViewModel);
