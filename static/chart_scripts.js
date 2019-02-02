function loadSetsLOTChart(labels, data, key, ctx){

ctx.destroy();

    ctx = new Chart(liftsOverTimectx, {
      type: 'line',
      data: {
          labels: labels,
          datasets:  getChartDatasetTEMP(data = data, key=key, fill=false, colors=true),
      },
      options: {
          scales: {
              yAxes: [{
                  ticks: {
                      beginAtZero:true,
                  }
              }],
              xAxes:[{
                  ticks: {
                      maxTicksLimit:10
                  },
                  type: 'time',
              }]
          },
          legend: {
              display: false
          },
          title: {
            display: true,
            text: 'Lifts Over Time',
            fontSize: 24,
          },
      },
    });

    return ctx
};