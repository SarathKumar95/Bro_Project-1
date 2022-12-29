

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


    // Testimonials carousel
    $(".testimonial-carousel").owlCarousel({
        autoplay: true,
        smartSpeed: 1000,
        items: 1,
        dots: true,
        loop: true,
        nav : false
    });


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
        },

        error: function (error_data){
            console.log(error_data)
            console.log("error")
        }
    });

    function mySales(){
        
    var ctx1 = $("#worldwide-sales").get(0).getContext("2d");
    var myChart1 = new Chart(ctx1, {
        type: "bar",
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
    var ctx2 = $("#salse-revenue").get(0).getContext("2d");
    var myChart2 = new Chart(ctx2, {
        type: "line",
        data: {
            labels: days,
            datasets: [{
                    label: "Salse",
                    data: day_order,
                    backgroundColor: "rgba(0, 156, 255, .5)",
                    fill: true
                },
                {
                    label: "Revenue",
                    data: [99, 135, 170, 130, 190, 180, 270],
                    backgroundColor: "rgba(0, 156, 255, .3)",
                    fill: true
                }
            ]
            },
        options: {
            responsive: true
        }
    });
    

    
})(jQuery);

