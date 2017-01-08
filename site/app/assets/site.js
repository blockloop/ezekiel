/* eslint-disable */

var graphData, graph;

function updateTemp() {
	$.getJSON("/api/current_temp", function (resp) {
		document.getElementById('currentTempNumber')
			.textContent = resp.probe_f
		document.getElementById('currentTempAsOf')
			.textContent = moment(resp.modified).format("MM/DD hh:mm:ss A")

		if (graphData && graphData.length > 0) {
			var latest = graphData[graphData.length-1];

			// stop unless the update is new
			if (! moment(resp.modified).isAfter(latest.modified)) {
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
	$.getJSON("/api/temps", function(resp) {
		graphData = resp.temperatures.map(function(t) {
			return [new Date(t.modified), t.probe_f];
		});

		var firstmtime = graphData[graphData.length-1][0];
		var lastmtime = graphData[0][0];

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
			xlabel: moment(firstmtime).format("MMM D hh:mm:ss A") + "<br/>TO<br/>" + moment(lastmtime).format("MMM D hh:mm:ss A"),
			ylabel: "Temperature °F"
		});
		// Update now and every 3s
		updateTemp();
		setInterval(updateTemp, 3000)

	});
});
