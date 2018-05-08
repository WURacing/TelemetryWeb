var path = null;
$(function(){

	// thanks stackoverflow
	google.maps.LatLng.prototype.kmTo = function (a) {
		var e = Math, ra = e.PI / 180;
		var b = this.lat() * ra, c = a.lat() * ra, d = b - c;
		var g = this.lng() * ra - a.lng() * ra;
		var f = 2 * e.asin(e.sqrt(e.pow(e.sin(d / 2), 2) + e.cos(b) * e.cos
		(c) * e.pow(e.sin(g / 2), 2)));
		return f * 6378.137;
	};
	google.maps.Polyline.prototype.inKm = function (n) {
		var a = this.getPath(n), len = a.getLength(), dist = 0;
		for (var i = 0; i < len - 1; i++) {
			dist += a.getAt(i).kmTo(a.getAt(i + 1));
		}
		return dist;
	};


	var socket = io.connect('http://' + document.domain + ':' + location.port);
	var lastLat = 0;
	var lastLng = 0;
	var change = true;

	socket.on('message', function(data) {
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
	});

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

		if (path.inKm() > 1) {
			coords.shift();
		}

		path.setMap(map);
	}
	update();

});

window.onbeforeunload = function(e) {
	socket.disconnect();
};