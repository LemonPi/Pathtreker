(function() {
var shutmedown = true;
var map;
var geocoder;

function geocodeName(geocode) {
	return geocode.address_components[0].short_name + geocode.address_components[1].short_name;
}

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
			$.get("/direction", "start=" + encodeURIComponent(geocodeName(startResult))
				+ "&end=" + encodeURIComponent(geocodeName(results[0])), handleDirectionResponse, "json")
			.fail(function() {
				alert("Network error");
			});
		});
	});
	return false;
}

function handleDirectionResponse(data, textStatus, jqXHR) {
	console.log(data);
}

function initUi() {
	$("#search-form").on("submit", submitForm);
}
function initMap() {
	initUi();
	geocoder = new google.maps.Geocoder();
	if (shutmedown) return;
	map = new google.maps.Map(document.getElementById("map"),
		{
			center: {lat: 43.6592125, lng: -79.4386709},
			zoom: 13
		});
}
window.initMap = initMap;
})();