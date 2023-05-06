
def chart(request):
    labels = []
    ordered = [] 
    delivered = []
    returned = []
    cancelled = []

    order_total = 0    
    deliver_total = 0
    return_total = 0
    cancel_total = 0

    today_order = len(Order.objects.filter(created_at=date.today()))
    period_order = 0

    start = 1
    end = 31
    month = date.today().month
    year = date.today().year

    total_revenue = 0
    today_revenue = 0

    deliver_price = 0
    return_price = 0
    cancel_price = 0

    if request.method == 'POST':
        fromDate = parse_date(request.POST['fromDate']) 
        toDate = parse_date(request.POST['toDate']) 

        year = fromDate.year
        month = fromDate.month 

        start = fromDate.day
        end =  toDate.day
    
    for day in range(start,end + 1):
        labels.append(day)
        order = Order.objects.filter(created_at=date.today().replace(day=day).replace(year=year).replace(month=month))

        for item in order:
            order_total+=item.total_price

        if len(order) == 0:
            ordered.append(0)
            
        else:
            ordered.append(len(order))
            period_order+=len(order)

      
        deliver = Order.objects.filter(status='Delivered').filter(created_at=date.today().replace(day=day).replace(year=year).replace(month=month)) 

        print("Delivered is ", deliver)

        for item in deliver:
            deliver_total+=item.total_price

        print("Del price is ",deliver_price) 


        if len(deliver) == 0:
            delivered.append(0)

        else:
            delivered.append(len(deliver))        

        returnOrders = Order.objects.filter(status='Returned').filter(created_at=date.today().replace(day=day).replace(year=year).replace(month=month))      

        for item in returnOrders:
            return_total+=item.total_price

        if len(returnOrders) == 0:
            returned.append(0)
        else:
            returned.append(len(returnOrders))

        cancel = Order.objects.filter(status='Cancelled').filter(created_at=date.today().replace(day=day).replace(year=year).replace(month=month))

        for item in cancel:
            cancel_total+=item.total_price

        if len(cancel) == 0:
            cancelled.append(0)

        else:
            cancelled.append(len(cancel))    

        piedata = [order_total,deliver_total,return_total,cancel_total]

        if deliver_total == 0:
            total_revenue = 0
        else:
            total_revenue = deliver_total - return_total


        delivered_today = Order.objects.filter(status='Delivered').filter(created_at=date.today())
        print("delivered today is ",delivered_today) 
        return_today = Order.objects.filter(status='Returned').filter(created_at=date.today())
        cancelled_today = Order.objects.filter(status='Cancelled').filter(created_at=date.today())

        for item in delivered_today:
            deliver_price+=item.total_price 

        
        for item in return_today:
            return_price+=item.total_price      

        print("Total rev is ", total_revenue) 

        print("Today's rev is ", today_revenue)

    return JsonResponse({"labels": labels, "ordered": ordered,
    "delivered":delivered,"returned":returned,
    "cancelled":cancelled,"piedata":piedata,
    "today_order":today_order,"period_total":period_order,
    "total_revenue":total_revenue,"todays_revenue":today_revenue})
