from django.http import HttpResponse
from django.shortcuts import redirect
from .models import User, Client, Subscription
import datetime
from django.shortcuts import render


t_delta = datetime.timedelta(days=30)
today = datetime.date.today()

def check_user_date(request)->bool:
    client = Client.objects.get(user=request.user)
    client_subscription = Subscription.objects.filter(client=client).select_related("client").order_by('-date_paid')
    try:
        last_time_paid = client_subscription[0].date_paid.date()
        expriation_day = last_time_paid + t_delta
        if expriation_day <= today:
            context = {'msg':'You need to pay for the subscription, subscription is over'}
            return render(request,'weather/no_subscription.html',context)
        else:
           return True
    except Exception as error:
        print(error)
        return error
       
  

def subscribed_member():
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            if request.user.is_superuser:
                print("Hello an admin!")
                return view_func(request, *args, **kwargs)
            else:  
                result =  check_user_date(request=request)
                if result == True:
                    return view_func(request, *args, **kwargs)
                else:
                     context = {'msg':"You do not have a subscription, you need to pay"}
                     return render(request,'weather/no_subscription.html',context)
        return wrapper_func
    return decorator
    