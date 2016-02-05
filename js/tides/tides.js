var tides = {
	urlBase: 'http://tidesandcurrents.noaa.gov/noaatidepredictions/NOAATidesFacade.jsp?Stationid=',
	stationID: '8725747',
    updateInterval: 20000,
    tideGraphLocation: '.tidegraph',
    tideTableLocation: '.tidetable'
}


/**
 * Retrieves the current temperature and weather patter from the OpenWeatherMap API
 */
tides.updateCurrentTides = function () {

	$.ajax({
		type: 'POST',
		url: 'tides.py',
		dataType: 'text',
		data: {'url': this.urlBase + this.stationID},
		success: function (response) {

		    var _newTideGraphHtml = '';
		    _newTideGraphHtml += response;

			$(this.tideGraphLocation).updateWithText(_newTideGraphHtml);

		}.bind(this),
		error: function () {

		    $(this.tideGraphLocation).updateWithText("Error!");

		}.bind(this)
	});

}

tides.init = function () {

	this.intervalId = setInterval(function () {
		this.updateCurrentTides();
	}.bind(this), this.updateInterval);

}