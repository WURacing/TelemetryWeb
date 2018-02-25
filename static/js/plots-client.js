/**
 * Starts the client and server pushing functionality
 */

var totalPoints = 50;
var serverUpdates = 100;
var source, dataset;
var now = new Date().getTime();
var somePlot = null;
var showData = [];
var map = null;

var options = {
    series: {
        lines: {
            lineWidth: 1.2,
            show: true
        }
    },
    legend: {
        show: false
    },
    xaxis: {
        show: false
    },
    yaxes: [
        {
            min: 0,
            max: 12500,
            tickSize: 500,
            axisLabelUseCanvas: true,
            axisLabelFontSizePixels: 12,
            axisLabelFontFamily: 'Verdana, Arial',
            axisLabelPadding: 6
        }, {
            min: 0,
            max: 100,
            show: false,
            position: "right",
            axisLabelUseCanvas: true,
            axisLabelFontSizePixels: 12,
            axisLabelFontFamily: 'Verdana, Arial',
            axisLabelPadding: 6
        }, {
            min: 0,
            max: 100,
            show: false,
            position: "right",
            axisLabelUseCanvas: true,
            axisLabelFontSizePixels: 12,
            axisLabelFontFamily: 'Verdana, Arial',
            axisLabelPadding: 6
        }, {
            min: 0,
            max: 200,
            show: false,
            position: "right",
            axisLabelUseCanvas: true,
            axisLabelFontSizePixels: 12,
            axisLabelFontFamily: 'Verdana, Arial',
            axisLabelPadding: 6
        }, {
            min: 0,
            max: 100,
            show: false,
            position: "right",
            axisLabelUseCanvas: true,
            axisLabelFontSizePixels: 12,
            axisLabelFontFamily: 'Verdana, Arial',
            axisLabelPadding: 6
        }, {
            min: 0,
            max: 90,
            show: false,
            position: "right",
            axisLabelUseCanvas: true,
            axisLabelFontSizePixels: 12,
            axisLabelFontFamily: 'Verdana, Arial',
            axisLabelPadding: 6
        }, {
            min: 0,
            max: 10,
            show: false,
            position: "right",
            axisLabelUseCanvas: true,
            axisLabelFontSizePixels: 12,
            axisLabelFontFamily: 'Verdana, Arial',
            axisLabelPadding: 6
        }, {
            min: 0,
            max: 13,
            show: false,
            position: "right",
            axisLabelUseCanvas: true,
            axisLabelFontSizePixels: 12,
            axisLabelFontFamily: 'Verdana, Arial',
            axisLabelPadding: 6
        }, {
            min: 0,
            max: 500,
            show: false,
            position: "right",
            axisLabelUseCanvas: true,
            axisLabelFontSizePixels: 12,
            axisLabelFontFamily: 'Verdana, Arial',
            axisLabelPadding: 6
        }, {
            min: 0,
            max: 500,
            show: false,
            position: "right",
            axisLabelUseCanvas: true,
            axisLabelFontSizePixels: 12,
            axisLabelFontFamily: 'Verdana, Arial',
            axisLabelPadding: 6
        }
    ]
};

function variablePoints(i){
    //primaries = [0, 1, 2, 8, 9];
    //secondaries = [3, 4, 5, 6, 7];
    /*if ("includes" in Array.prototype){
        if (primaries.includes(i)){
            return 5*totalPoints;
        }
        else if (secondaries.includes(i)){
            return totalPoints;
        }
    }
    else{
        return totalPoints
    }*/
    if ((i >= 0 && i <= 2) || i == 8 || i == 9){
        return 5*totalPoints;
    }
    else{
        return totalPoints;
    }
}

function initData() {
    var numSeries = 10;
    var dataSeries = [];
    for (var i = 0; i < numSeries; i++) {
        dataSeries[i] = [];
    }
    for (var i = 0; i < totalPoints; i++) {
        var temp = [now += serverUpdates, 0];
 
        for (var j = 0; j < numSeries; j++) {
            dataSeries[j].push(temp);
        }
    }

    dataset = [
        { label: "RPMs",                    data: dataSeries[0], lines: { lineWidth: 1.2 }, color: "#00FF00", yaxis: 1, idx: 0 },
        { label: "Engine Load (%)",         data: dataSeries[1], lines: { lineWidth: 1.2 }, color: "#0044FF", yaxis: 2, idx: 1 },
        { label: "Throttle (%)",            data: dataSeries[2], lines: { lineWidth: 1.2 }, color: "#FF0000", yaxis: 3, idx: 2 },
        { label: "Coolant Temperature (C)", data: dataSeries[3], lines: { lineWidth: 1.2 }, color: "#551A8B", yaxis: 4, idx: 3 },
        { label: "Oxygen",                  data: dataSeries[4], lines: { lineWidth: 1.2 }, color: "#FFA500", yaxis: 5, idx: 4 },
        { label: "Vehicle Speed (mph)",     data: dataSeries[5], lines: { lineWidth: 1.2 }, color: "#FF69B4", yaxis: 6, idx: 5 },
        { label: "Gear",                    data: dataSeries[6], lines: { lineWidth: 1.2 }, color: "#008080", yaxis: 7, idx: 6 },
        { label: "Battery Voltage (V)",     data: dataSeries[7], lines: { lineWidth: 1.2 }, color: "#228B22", yaxis: 8, idx: 7 },
        { label: "Right Rear Potentiometer",data: dataSeries[8], lines: { lineWidth: 1.2 }, color: "#104AAE", yaxis: 9, idx: 8 },
        { label: "Left Rear Potentiometer", data: dataSeries[9], lines: { lineWidth: 1.2 }, color: "#AE10A7", yaxis: 10, idx: 9 }
    ];
    map = { "RPMs":     0,
            "Load":     1, 
            "Throttle": 2, 
            "Coolant":  3, 
            "O2":       4, 
            "Speed":    5, 
            "Gear":     6, 
            "Volts":    7, 
            "RRPot":    8, 
            "RLPot":    9
    };
    for (var i = 0; i < dataset.length; i++) {
        showData[i] = true;
    }
}
var startClientServer = function() {

    //Get the URL to hand into the connect call
    /*var http = location.protocol;
    var slashes = http.concat("//");
    var host = slashes.concat(window.location.hostname);*/

    source = new EventSource('/stream');


    //socket.emit('updateInterval', serverUpdates);
    /*
     * Repaint graph function.  This repaints the graph
     * at a timed interval
     */
    function repaintGraph(now, _data) {
        var someData = somePlot.getData();
        var temp;
        /*for (var i = 0; i < someData.length; i++) {
            someData[i].data.shift();
            temp = [_data[0], _data[i+1]];
            someData[i].data.push(temp);
            // someData[i].data = simplify(dataSeries[i], .08, true);
            // console.log(dataSeries[i]);
            // console.log(someData[i].data);
            someData[i].lines.show = showData[i];
        }*/
        for (var key in _data){
            if (_data.hasOwnProperty(key) && map.hasOwnProperty(key)){
                var i = map[key];
                if (someData[i].data.length >= variablePoints(i)){
                    someData[i].data.shift();
                }
                temp = [now, _data[key]];
                someData[i].data.push(temp);
                someData[i].lines.show = showData[i];
            }
        }
        somePlot.setData(someData);
        somePlot.setupGrid();
        somePlot.draw();
    }

    /*
     * Receiving data from the server
     */
    source.addEventListener('dashboard', function omg(event) {
		data = JSON.parse(event.data);
		repaintGraph(Date.now(), data);
    }, false);


    /*socket.on('connect', function(e) {
        socket.emit('updateInterval', serverUpdates);
    });*/

    togglePlot = function(seriesIdx)
    {
        // console.log(showData[seriesIdx]);
        showData[seriesIdx] = !showData[seriesIdx];
    }
};

$(document).ready(function () {
    initData();
    somePlot = $.plot($("#placeholder"), dataset, options);
    startClientServer();
    $.each(dataset, function(key, val) {
        l = val.label;
        var li = $('<li />').appendTo($("#overviewLegend"));
        
        $('<input name="' + l + '" id="' + val.idx + '" class="checkbox" type="checkbox" checked="checked" /><div class="colorTile"><div style="width:4px;height:0;border:5px solid ' + val.color + ';overflow:hidden"></div></div>').appendTo(li);
        $('<label>', {
            text: l, 
            'for': l
        }).appendTo(li);
    });
    $(".checkbox").change(function() {
        var idx = Number(this.id);
        togglePlot(idx);
    });
    $('.legendColorBox > div').each(function(i){
        $(this).clone().prependTo(choiceContainer.find("li").eq(i));
    });
    window.onresize = function(event) {
        somePlot = $.plot($("#placeholder"), somePlot.getData(), options);
    }
});
window.onbeforeunload = function(e) {
    source.close();
};