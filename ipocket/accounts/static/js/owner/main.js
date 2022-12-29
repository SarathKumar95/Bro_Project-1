

(function ($) {
    "use strict";

    // Spinner
    var spinner = function () {
        setTimeout(function () {
            if ($('#spinner').length > 0) {
                $('#spinner').removeClass('show');
            }
        }, 1);
    };
    spinner();
    
    
    // Back to top button
    $(window).scroll(function () {
        if ($(this).scrollTop() > 300) {
            $('.back-to-top').fadeIn('slow');
        } else {
            $('.back-to-top').fadeOut('slow');
        }
    });
    $('.back-to-top').click(function () {
        $('html, body').animate({scrollTop: 0}, 1500, 'easeInOutExpo');
        return false;
    });


    // Sidebar Toggler
    $('.sidebar-toggler').click(function () {
        $('.sidebar, .content').toggleClass("open");
        return false;
    });


    // Progress Bar
    $('.pg-bar').waypoint(function () {
        $('.progress .progress-bar').each(function () {
            $(this).css("width", $(this).attr("aria-valuenow") + '%');
        });
    }, {offset: '80%'});


    // Calender
    $('#calender').datetimepicker({
        inline: true,
        format: 'L'
    });



    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    const csrftoken = getCookie('csrftoken');

    // Worldwide Sales Chart

    var endpoint = '/chart'
    let labels = []
    let ordered = [] 
    let delivered = []
    let returned = []
    let cancelled = [] 
    
    $.ajax({
        method : "GET",
        url: endpoint,
        success: function (response) {
            labels = response.labels
            ordered = response.ordered
            delivered = response.delivered
            returned = response.returned
            cancelled = response.cancelled
            mySales() 

            document.getElementById('todays-revenue').innerText = response.todays_revenue
            document.getElementById('monthly_order').innerText = response.period_total
            document.getElementById('monthrev').innerText =  response.total_revenue           
            document.getElementById('todayOrder').innerText = response.today_order              
        },

        error: function (error_data){
            console.log(error_data)
            console.log("error")
        }
    });

    $('#filter-form').submit(function (e) { 
        e.preventDefault();
        let fromDate = document.getElementById('from_date').value 
        let toDate = document.getElementById('to_date').value    
    
        $.ajax({
            method:"POST",
            url: endpoint,
            data: {
                'fromDate':fromDate,
                'toDate' : toDate,
                csrfmiddlewaretoken:csrftoken
            },
            success: function (response) {
                console.log("Labels is",response.labels);
                ordered = response.ordered
                delivered = response.delivered
                returned = response.returned
                cancelled = response.cancelled
                labels = response.labels
                piedata = response.piedata
                
                let allzero = piedata.every(item => item == 0); 

                if(allzero == true){
                    document.getElementById('dataCheck').hidden = false                    
                }

                else{
                    document.getElementById('dataCheck').hidden = true
                }
                
                

                let chartStatus = Chart.getChart("worldwide-sales"); // <canvas> id
                
                if (chartStatus != undefined) {
                    chartStatus.destroy();
                }

                
                let chartPie = Chart.getChart("salse-revenue"); // <canvas> id
                
                if (chartPie != undefined) {
                    chartPie.destroy();
                }

                document.getElementById('from_dateText').innerText = fromDate
                document.getElementById('to_dateText').innerText = toDate
                document.getElementById('monthrev').innerText =  response.total_revenue
                document.getElementById('monthly_order').innerText = response.period_total

                mySales()
                myPie()
                 
            }
        });
    });
    function mySales(){
        
    var ctx1 = $("#worldwide-sales").get(0).getContext("2d");
    
    var myChart1 = new Chart(ctx1, {
        type: "line",
        data: {
            labels: labels,
            datasets: [{
                    label: "Orders",
                    data:ordered,
                    backgroundColor: "rgba(55, 109, 255, 0.62)"
                },
                
                {
                    label: "Delivered",
                    data:delivered ,
                    backgroundColor: "rgba(0, 255, 52, 0.5)"
                },
                {
                    label: "Returned",
                    data: returned,
                    backgroundColor: "rgb(192,192,192)"
                },
                {
                    label: "Cancelled",
                    data: cancelled,
                    backgroundColor: "rgba(255, 40, 39, 0.62)"
                }
            ],
            },
        options: {
            responsive: true
        }
        
    });

    }
    
    // Salse & Revenue Chart 

    let piedata = []

    $.ajax({
        method : "GET",
        url: endpoint,
        success: function (response) {
            piedata = response.piedata
            myPie() 
        }
    });
    

    function myPie(){
        var ctx2 = $("#salse-revenue").get(0).getContext("2d");
        var myChart2 = new Chart(ctx2, {
        type: "doughnut",
        data: {
            labels: ["Orders", "Delivered","Returned","Cancelled"] ,
            datasets: [{
                    label: "Sales",
                    data: piedata,
                    backgroundColor: [
                                     'rgb(255, 205, 86)',   
                                     'rgba(0, 255, 52, 0.5)',   
                                     'rgb(54, 162, 235)',
                                     'rgb(255, 99, 132)',
                                     
            ]
                },
            ]
            },
        options: {
            responsive: true
        }
    });
    


    }
    
    
})(jQuery);

