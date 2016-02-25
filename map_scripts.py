# -*- coding: utf-8 -*-
"""
Created on Mon Feb 8 15:14:15 2016

@author: kate
"""

# to render html
from IPython.display import HTML

def plot_markers(data):
	# so we can see google maps
	style = """
		<style>
				html, body {
					height: 100%;
					margin: 0;
					padding: 0;
				}
				#map {
					height: 500px;
					margin-right: 400px;
				}
				#floating-Panel {
					position: absolute;
					top: 10px;
					left: 25%;
					z-index: 5;
					background-color: #fff;
					padding: 5px;
					border: 1px solid #999;
					text-align: center;
					font-family: 'Roboto','sans-serif';
					line-height: 30px;
					padding-left: 10px;
					background: #fff;
					padding: 5px;
					font-size: 14px;
					font-family: Arial;
					border: 1px solid #ccc;
					box-shadow: 0 2px 2px rgba(33, 33, 33, 0.4);
				}
				#directions-Panel {
					font-family: 'Roboto','sans-serif';
					line-height: 30px;
					padding-left: 10px;
					height: 500px;
					float: right;
					width: 390px;
					overflow: auto;
				}
				#directions-Panel select, #directions-Panel input {
					font-size: 15px;
				}

				#directions-Panel select {
					width: 100%;
				}

				#directions-Panel i {
					font-size: 12px;
				}
				#other-places-Panel {
					overflow: auto;
				}
		</style>
	"""

	javascript_asnc = """
	<script async defer
			src="https://maps.googleapis.com/maps/api/js?key=AIzaSyDSVmwM_JIMJx3WebgRC6JmEHkt6FvIKCg&callback=initMap">
	</script>
	"""

	input_form = """
	<div id="floating-Panel">
	<input id="start"></input>
	<button onclick="onChangeHandler()">Find Closest</button>
    </div>
	<div id="directions-Panel"> </div>
	<div id="map"> </div>
	<div id="other-places-Panel">
	</div>
	"""

	javascript = """
	<script type="text/Javascript">
			function geocodeAddress(address, name, geocoder, resultsMap, markersArray) {
					geocoder.geocode({'address': address}, function(results, status) {
							if (status === google.maps.GeocoderStatus.OK) {
									var location = results[0].geometry.location;
									resultsMap.setCenter(location);
									var marker = new google.maps.Marker({
											map: resultsMap,
											title: name,
											position: location
									});
									var infowindow = new google.maps.InfoWindow({
										content: name + '<br/>' + address
									});
									infoWindows.push(infowindow);
									marker.addListener('click', function() {
										deleteInfoWindows();
										infowindow.open(resultsMap, marker);
									});
									markersArray.push(marker);
							} else {
									alert('Geocode was not successful for the following reason: ' + status);
							}
					});
			}
			
			function deleteInfoWindows() {
				for (var i=0; i < infoWindows.length; i++) {
					infoWindows[i].close();
				}
			}
			
			function putAddress(lat_long_pair, name, resultsMap) {
					return new google.maps.Marker({
							map: resultsMap,
							title: name,
							position: {lat: lat_long_pair[0], lng: lat_long_pair[1]}
					});
			}
			
			function calculateAndDisplayRoute(start, end) {
				directionsService.route({
					origin: start,
					destination: end,
					travelMode: google.maps.TravelMode.DRIVING
				}, function(response, status) {
					if (status === google.maps.DirectionsStatus.OK) {
						directionsDisplay.setDirections(response);
					} else {
						window.alert('Directions request failed due to ' + status);
					}
				});
			}
			
			var map;
			var markers = Array();
			var infoWindows = Array();
			var service;
			var directionsDisplay;
			var directionsService;
			
			function initMap() {
					map = new google.maps.Map(document.getElementById('map'), {
									zoom: 10
							});
					var geocoder = new google.maps.Geocoder();
					service = new google.maps.DistanceMatrixService;
					directionsService = new google.maps.DirectionsService;
					directionsDisplay = new google.maps.DirectionsRenderer;
					directionsDisplay.setMap(map);
					directionsDisplay.setPanel(document.getElementById('directions-Panel'));
	
	"""
	
	javascript += get_marker_text(data)
	
	javascript += """
			}
			
	function onChangeHandler() {
		var locations = [];
		for (var i = 0; i < markers.length; i++) {
			locations.push({lat: markers[i].position.lat(), lng: markers[i].position.lng(), title: markers[i].title});
		}
		service.getDistanceMatrix({
			origins: [document.getElementById('start').value],
			destinations: locations,
			travelMode: google.maps.TravelMode.DRIVING,
			unitSystem: google.maps.UnitSystem.IMPERIAL,
			avoidHighways: false,
			avoidTolls: false
		}, function(response, status) {
			if (status !== google.maps.DistanceMatrixStatus.OK) {
				alert('error was: ' + status);
			} else {
				var origin = response.originAddresses[0];
				var destinationlist = locations;
				var outputdiv = document.getElementById('other-places-Panel');
				outputdiv.innerHTML = '';
				
				var distances = response.rows[0].elements;
				var results = Array();
				for (var j = 0; j < distances.length; j++) {
					results.push({'loc':destinationlist[j], 'dist': distances[j]});
				}
				results.sort(function(a,b) {
					if (a.dist.duration.text == b.dist.duration.text) {
						if (a.dist.distance.value > b.dist.distance.value) return 1;
						if (a.dist.distance.value < b.dist.distance.value) return -1;
					}
					if (a.dist.duration.value > b.dist.duration.value) return 1;
					if (a.dist.duration.value < b.dist.duration.value) return -1;
					return 0
				});
				for (var j = 0; j < results.length; j++) {
					outputdiv.innerHTML += results[j].dist.distance.text + ' in ' +
							results[j].dist.duration.text + ' to ' + results[j].loc.title + '<br>';
				}
				
				calculateAndDisplayRoute(origin, results[0].loc);
			}
		});
	}

	</script>
	"""

	return style + input_form + javascript + javascript_asnc

def get_marker_text(data):
	lat_long_javascript = ''
	for i in range(len(data)):
		location = data['Location'][i]
		if type(location) == tuple:
			lat_long_javascript += """
					markers.push(putAddress('"""+str(location)+"""', '"""+data['Name'][i]+"""', geocoder, map));
			"""
		else:
			lat_long_javascript += """
					geocodeAddress('"""+location.replace('\n', ' ')+"""', '"""+data['Name'][i]+"""', geocoder, map, markers);
			"""
	return lat_long_javascript
