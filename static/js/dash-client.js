var source;
$(function(){

	var decimalPlaces = new Object();
	$(".data").each(function(){
		decimalPlaces[$(this).attr("id")] = $(this).attr("decimals");
	});

	source = new EventSource('/stream');
	source.addEventListener('dashboard', function omg(event) {
		data = JSON.parse(event.data);
		for (var key in data){
			if (data.hasOwnProperty(key)){
				$("#"+key).text(data[key].toFixed(decimalPlaces[key]));
			}
		}
    }, false);

	function rotate(){

		//console.log("called rotate");

		var rpm = parseInt($("#RPMs").text(), 10);
		if(rpm || rpm == 0){
			var deg = (rpm/12000.0) * 309.0;

			deg = ((deg <= 309.0) ? deg : 309.0).toFixed(0);

			var dial = document.getElementById('dial');

		    dial.style.webkitTransform = 'rotate('+deg+'deg)'; 
		    dial.style.mozTransform    = 'rotate('+deg+'deg)'; 
		    dial.style.msTransform     = 'rotate('+deg+'deg)'; 
		    dial.style.oTransform      = 'rotate('+deg+'deg)'; 
		    dial.style.transform       = 'rotate('+deg+'deg)'; 
		}
	}

	setInterval(rotate, 500);

});

window.onbeforeunload = function(e) {
    source.close();
};