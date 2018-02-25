var source;
$(function(){

	var lastLat = 0;
	var lastLng = 0;
	var path = null;
	var change = true;

	source = new EventSource('/stream');

	source.addEventListener('maps', function omg(event) {
		data = JSON.parse(event.data);
		for (var key in data) {
			if (!data.hasOwnProperty(key)) {
				continue;
            }
			var num = data[key];
			console.log(key + " " + num);
			if (key === "lat" && Math.abs(num) > 1 && num !== lastLat) {
				lastLat = num;
				change = true;
			} else if (key === "lng" && Math.abs(num) > 1 && num !== lastLng) {
				lastLng = num;
				change = true;
			}
		}
		if (change) {
			update();
			change = false;
		}
	}, false);

	function update() {
		console.log("Updating map");
        if (path !== null) {
			path.setMap(null);
		}

		if (lastLat !== 0 && lastLng !== 0) {
            coords.push(new google.maps.LatLng(lastLat, lastLng));
        }

        path = new google.maps.Polyline({
            clickable: false,
            geodesic: true,
            path: coords,
            strokeColor: "#6495ED",
            strokeOpacity: 1.000000,
            strokeWeight: 10
        });

        path.setMap(map);
	}
	update();

});

window.onbeforeunload = function(e) {
    source.close();
};