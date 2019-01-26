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


<!--var daysMonthctx = document.getElementById("daysPerMonthChart");-->
<!--var daysPerMonthChart = new Chart(daysMonthctx, {-->
<!--type: 'line',-->
<!--data: {-->
    <!--labels: [1, 2, 3, 4, 5, 6, ,7 8, 9, 10, 11, 12],-->
    <!--datasets: [{-->
        <!--label: 'Days Exercised Per Month 2017',-->
        <!--data: [-->
            <!--{% for v in dpv %}"{{ v }}",{% endfor %}-->
        <!--],-->
    <!--},{-->
        <!--label: 'Days Exercised Per Month 2018',-->
        <!--data: [-->
        <!--],-->
    <!--},{-->
        <!--label: 'Days Exercised Per Month 2019',-->
        <!--data : [-->
        <!--],-->
    <!--}]-->
<!--},-->
<!--options: {-->
    <!--scales: {-->
        <!--yAxes: [{-->
            <!--ticks: {-->
                <!--beginAtZero:true-->
            <!--}-->
        <!--}]-->
    <!--}-->
<!--}-->
<!--});-->