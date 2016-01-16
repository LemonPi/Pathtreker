(function() {
/**
 * The main Google Maps instance.
 * @type google.maps.Map
 */
var map;
/**
 * The previous path overlaid on the map, if any.
 * @type google.maps.Polyline
 */
var oldPolyline;
/**
 * The main Google Maps Geocoder instance.
 * @type google.maps.Geocoder
 */ 
var geocoder;

/**
 * Gets the short name containing house number and street name from a GeocoderResult
 */

function geocodeName(geocode) {
	return geocode.address_components[0].short_name + " " + geocode.address_components[1].short_name;
}

/**
 * Stores the canonized start and end address of the last query.
 */

var lastQuery = {};

/**
 * Translates side IDs from the API to human-readable sides.
 */
var sides = {"L": "left", "R": "right"}

/**
 * Rounds a number to two decimal points.
 */

function roundtotwopoints(a) {
	return Math.round(a * 100) / 100;
}

/**
 * Displays a kilometer value intellgently: if the value is less than 1.5 km,
 * return the value converted to meters and rounded to two decimal places,
 * otherwise round the kilometer values to two decimal place
 */

function rounddist(a) {
	if (a < 1.5) {
		return roundtotwopoints(a * 1000) + " m";
	}
	return roundtotwopoints(a) + " km";
}

/**
 * Canonize addresses and submits form to server.
 */

function submitForm() {
	// Canonize address through Google Maps Geocoding API
	var searchStart = $("#search-form input[name='start']")[0].value;
	var searchEnd = $("#search-form input[name='end']")[0].value;
	var restrictions = {
		country: "CA",
		locality: "Toronto"
	};
	var startResult;
	geocoder.geocode({
		address: searchStart,
		componentRestrictions: restrictions
	}, function(results, status) {
		if (status != google.maps.GeocoderStatus.OK || results.length == 0) {
			alert("start address is invalid");
			return;
		}
		startResult = results[0];
		geocoder.geocode({
			address: searchEnd,
			componentRestrictions: restrictions
		}, function(results, status) {
			if (status != google.maps.GeocoderStatus.OK || results.length == 0 ) {
				alert("end address is invalid");
				return;
			}
			lastQuery.start = geocodeName(startResult);
			lastQuery.end = geocodeName(results[0]);
			$.get("/direction", "start=" + encodeURIComponent(lastQuery.start)
				+ "&end=" + encodeURIComponent(lastQuery.end), handleDirectionResponse, "json")
			.fail(function() {
				alert("Network error");
			});
		});
	});
	return false;
}


/**
 * Update interface and map from server response.
 */
function handleDirectionResponse(data, textStatus, jqXHR) {
	//console.log(data);
	if (data.error != null) {
		alert(data.error);
		return;
	}
	$("#direction-length").text("Total distance: " + rounddist(data.length) + '\n');
	var parts = [];
	var lines = [];
	var bounds = new google.maps.LatLngBounds();
	for (var i = 0; i < data.path.length; i++) {
		var p = data.path[i];
		if (p.action == "along") {
			parts.push($("<div>").text("Head " + p.direction + " along " + p.from.name + " to " + p.to.name));
			lines.push({lat: p.from.lat, lng: p.from.lon});
			lines.push({lat: p.to.lat, lng: p.to.lon});
			bounds.extend(new google.maps.LatLng({lat: p.from.lat, lng: p.from.lon}))
			bounds.extend(new google.maps.LatLng({lat: p.to.lat, lng: p.to.lon}))
		} else if (p.action == "turn") {
			parts.push($("<div>").text("Turn " +
				p.direction + " onto " + p.to.name));
		} else if (p.action == "arrive") {
			parts.push($("<div>").text(lastQuery.end + " is on the " + sides[p.side]));
		}
		if (p.distance) {
			parts.push($("<div>").text("(" + rounddist(p.distance) + ")").addClass("distances"));
		}
		parts.push($("<hr>"));
	}
	$("#directions").empty().append(parts);
	var thepolyline = new google.maps.Polyline({
		path: lines,
		geodesic: true,
		strokeColor: '#FF0000',
		strokeOpacity: 1.0,
		strokeWeight: 2
	});
	if (oldPolyline != null) {
		oldPolyline.setMap(null);
	}
	thepolyline.setMap(map);
	oldPolyline = thepolyline;
	map.fitBounds(bounds);
}

/**
 * Initializes user interface at startup.
 */
function initUi() {
	$("#search-form").on("submit", submitForm);
}

/**
 * Called by Google Maps API to initialize the map
 */
function initMap() {
	initUi();
	geocoder = new google.maps.Geocoder();
	map = new google.maps.Map(document.getElementById("map"),
		{
			center: {lat: 43.6592125, lng: -79.4386709},
			zoom: 13
		});
}
window.initMap = initMap;
})();