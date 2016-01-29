<html>
<head>
	<title>Tide Predictor</title>
	<style type="text/css">
		<?php include('css/main.css') ?>
	</style>
	<link rel="stylesheet" type="text/css" href="css/weather-icons.css">
	<script type="text/javascript">
		var gitHash = '<?php echo trim(`git rev-parse HEAD`) ?>';
	</script>
	<meta name="google" value="notranslate" />
	<meta http-equiv="Content-type" content="text/html; charset=utf-8" />
</head>
<body>

	<div class="top left">
	    <div class="date small dimmed"></div>
	    <div class="time"></div>
	    <div class="windsun small dimmed"></div>
	    <div class="temp"></div>
	    <div class="forecast small dimmed"></div>
	</div>
	<div class="top right">
	    <div class="tidetable small dimmed">Tide Table</div>
	</div>
	<div class="center-ver center-hor"><div class="tidegraph">
	<img src="http://tidesandcurrents.noaa.gov/noaatidepredictions/serveimage?filename=images/8725747/27012016/541/8725747_2016-01-28.gif">
	</div></div>
	<!--
	<div class="lower-third center-hor"><div class="compliment light"></div></div>
	<div class="bottom center-hor"><div class="news medium"></div></div>
	-->


<script src="js/jquery.js"></script>
<script src="js/jquery.feedToJSON.js"></script>
<script src="js/ical_parser.js"></script>
<script src="js/moment-with-locales.min.js"></script>
<script src="js/config.js"></script>
<script src="js/rrule.js"></script>
<script src="js/version/version.js"></script>
<script src="js/calendar/calendar.js"></script>
<script src="js/compliments/compliments.js"></script>
<script src="js/weather/weather.js"></script>
<script src="js/time/time.js"></script>
<script src="js/news/news.js"></script>
<script src="js/tides/tides.js"></script>
<script src="js/main.js?nocache=<?php echo md5(microtime()) ?>"></script>
<!-- <script src="js/socket.io.min.js"></script> -->
</body>
</html>