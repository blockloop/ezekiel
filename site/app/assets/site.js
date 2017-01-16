/* eslint-disable */

var graphData, graph;
var lock = 0;

function updateTemp() {
	$.getJSON("/api/current_temp", function (resp) {
		document.getElementById('currentTempNumber')
			.textContent = resp.probe_f
		document.getElementById('currentTempAsOf')
			.textContent = moment(resp.modified).format("MM/DD hh:mm:ss A")

		if (graphData && graphData.length > 0) {
			var latest = graphData[graphData.length-1];

			// stop unless the update is new
			if (! moment(resp.modified).isAfter(latest[0])) {
				return;
			}

			graphData.push([new Date(resp.modified), resp.probe_f])
			if (graph) {
				graph.updateOptions( { 'file': graphData } );
			}
		}
	})
}

$(function() {
	// Update now and every 3s
	updateTemp();
	setInterval(updateTemp, 3000);
	$('#go-btn').click(setTemps);
	$('form').submit(function() {
		setTemps();
		return false;
	});
	setTemps();
});

function setTemps() {
	var qs = {};
	var since = $('#lastHours').val()
	if (since != null) {
		qs.since = moment().subtract(since, 'hours').utc().format();
	}

	$.getJSON("/api/temps", qs, function(resp) {
		graphData = resp.temperatures.map(function(t) {
			return [new Date(t.modified), t.probe_f];
		});

		graph = new Dygraph(document.getElementById("tempChart"), graphData, {
			title: "Historical Temperatures",
			axes: {
				x: {
					valueFormatter: function(x) {
						return moment(x).format("MMM D hh:mm:ss A")
					}
				},
				y: {
					valueFormatter: function(x) {
						return ""+x+"&deg;F";
					}
				}
			},
			animatedZooms: true,
			drawPoints: false,
			strokeWidth: 3,
			strokeBorderWidth: 1,
			highlightCircleSize: 5,
			fillGraph: true,
			ylabel: "Temperature °F"
		});

	});
}
