var tides = {
	urlBase: 'http://tidesandcurrents.noaa.gov/noaatidepredictions/NOAATidesFacade.jsp?Stationid=',
	stationID: '8725747',
    updateInterval: 6000,
    tideGraphLocation: '.tidegraph',
    tideTableLocation: '.tidetable'
}


var url = "py/tides.png"; //url to load image from
var refreshInterval = 1000; //in ms
var drawDate = true; //draw date string
var img;

tides.init = function () {
    var canvas = document.getElementById("canvas");
    var context = canvas.getContext("2d");
    img = new Image();
    img.onload = function() {
        canvas.setAttribute("width", img.width)
        canvas.setAttribute("height", img.height)
        context.drawImage(this, 0, 0);
        if(drawDate) {
            var now = new Date();
            var text = now.toLocaleDateString() + " " + now.toLocaleTimeString();
            var maxWidth = 100;
            var x = img.width-10-maxWidth;
            var y = img.height-10;
            context.strokeStyle = 'black';
            context.lineWidth = 2;
            context.strokeText(text, x, y, maxWidth);
            context.fillStyle = 'white';
            context.fillText(text, x, y, maxWidth);
        }
    };
    refresh();
}
function refresh()
{
    img.src = url + "?t=" + new Date().getTime();
    setTimeout("refresh()",refreshInterval);
}


/**
 * Retrieves the current temperature and weather patter from the OpenWeatherMap API
 */
/*
tides.updateCurrentTides = function () {

	$.ajax({
		type: 'POST',
		url: 'tides.py',
		dataType: 'text',
		success: function (response) {

		    var _newTideGraphHtml = '';
		    _newTideGraphHtml += response;

			$(this.tideGraphLocation).updateWithText(_newTideGraphHtml);

		}.bind(this),
		error: function () {

		    $(this.tideGraphLocation).updateWithText('<img src="py/tides.png">');

		}.bind(this)
	});

}

tides.init = function () {

	this.intervalId = setInterval(function () {
		this.updateCurrentTides();
	}.bind(this), this.updateInterval);

}
*/