var daysYearctx = document.getElementById("daysPerYearChart");
var daysPerYearChart = new Chart(daysYearctx, {
    type: 'bar',
    data: {
        labels: ["2017", "2018", "2019"],
        datasets: [{
            label: 'Days Exercised Per Year',
            data: [31, 208, 12],
        }]
    },
    options: {
        scales: {
            yAxes: [{
                ticks: {
                    beginAtZero:true
                }
            }]
        }
    }
});



var daysPerMonthChart = new Chart(daysMonthctx, {
type: 'line',
data: {
    labels: ["January", "February", "March", "April", "May", "June", "July",
            "August", "September", "October", "November", "December"],
    datasets: [{
        label: 'Days Exercised Per Month 2017',
        fill: false,
        backgroundColor: getThemeColor(0),
        borderColor: getThemeColor(0),
        data: [{
           x: "July",
           y: 5
        }, {
            x: "August",
            y: 5
        }],
    },{
        label: 'Days Exercised Per Month 2018',
        fill: false,
        backgroundColor: getThemeColor(1),
        borderColor: getThemeColor(1),
        data: [{
           x: "January",
           y: 19
        }, {
            x: "February",
            y: 16
        }, {
            x: "March",
            y: 19
        }, {
            x: "April",
            y: 13
        }],
    },{
        label: 'Days Exercised Per Month 2019',
        fill: false,
        backgroundColor: getThemeColor(2),
        borderColor: getThemeColor(2),
        data: [{
           x: "January",
           y: 12
        }]
    }]
},
options: {
    responsive: true,
    title: {
        display: true,
        text: 'Days Exercised per Month'
    },
}
});


//<!--Need function for this-->
var liftData = {{ lot_dict|safe }}
var lifts = Object.keys({{ lot_dict|safe }});
datasetData = [];
for (var i = 0; i < Object.keys(liftData).length; i++){
datasetData[i] = {
    label: lifts[i],
    fill: false,
    lineTension: 0,
    <!--backgroundColor: themeColors[i],-->
    <!--borderColor: themeColors[i],-->
    data: liftData[lifts[i]]
}
}


<!--Create dataset based on data pased from flask-->
var dataPoints = {{ dpm_dict|safe }} // variable for data sent from flask
var years = Object.keys({{ dpm_dict|safe }}); //variable for keys sent from flask
var datasetData = []; //variable for returned list
for (var i = 0; i < Object.keys(dataPoints).length; i++){
datasetData[i] = {
    label: 'Days Exercised Per Month in DataYear'.replace('DataYear', years[i]),
    fill: false,
    backgroundColor: themeColors[i],
    borderColor: themeColors[i],
    data: dataPoints[years[i]]
}
}

