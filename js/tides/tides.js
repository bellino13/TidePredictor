var tides = {
	urlBase: 'http://tidesandcurrents.noaa.gov/noaatidepredictions/NOAATidesFacade.jsp?Stationid=',
	stationID: '8725747',
    updateInterval: config.tides.interval,
    tideGraphLocation: '.tidegraph',
    tideTableLocation: '.tidetable'
}


/**
 * Retrieves the current temperature and weather patter from the OpenWeatherMap API
 */
tides.updateCurrentTides = function () {

	$.ajax({
		type: 'POST',
		url: '../py/tides.py',
		dataType: 'text',
		/*data: {url: this.urlBase + this.stationID},*/
		success: function (response) {

		    var _newTideGraphHtml = '';
		    _newTideGraphHtml += response;

			$(this.tideGraphLocation).updateWithText(_newTideGraphHtml, this.fadeInterval);

		}.bind(this),
		error: function () {

		}
	});

}

tides.init = function () {

	this.intervalId = setInterval(function () {
		this.updateCurrentTides();
	}.bind(this), this.updateInterval);

}