from django.shortcuts import render
from django.http import HttpResponse
import requests
from .models import City, Client, BankAccount, Subscription
from .forms import CityForm, BankForm
from .decorators import subscribed_member
import datetime
from django.shortcuts import redirect
from django.views.generic.edit import CreateView
# Create your views here.


def check_db_city(city_name: str):
    try:
        db_city = City.objects.get(name=city_name)
        return True
    except:
        return False

def weather_date():
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=219b58b008da2b4c6be2ff72d76be973'
    cities = City.objects.all()
    weather_data = []
    for city in cities:
        try:
            r = requests.get(url.format(city)).json()
            city_weather = {
                'city' : city.name,
                'temperature' : r['main']['temp'],
                'description' : r['weather'][0]['description'],
                'icon' : r['weather'][0]['icon'],
            }

            weather_data.append(city_weather)
        except:
            return HttpResponse("500,Internal server error!")
    return weather_data

@subscribed_member()
def index(request):
    if request.method == 'POST':
        form = CityForm(request.POST)
        city_name = request.POST['name']
        db_city = check_db_city(city_name=city_name)
        if db_city:
            return HttpResponse(f"{city_name} already exists!")
        form.save()

    form = CityForm()
    weather_data = weather_date()   
    context = {'weather_data':weather_data,'form' : form}
    return render(request, 'weather/main.html',context)


    

def check_db_bank_account(client):
    try:
        bank_account = BankAccount.objects.get(client=client)
        return True
    except:
        return False


def pay_subsctiption(request, client):
    Subscription.objects.create(client=client,date_paid=datetime.datetime.today())
    return True


def subscription_page(request):
    if request.method == 'POST':
        form = BankForm(request.POST)
        instance = form.save(commit=False)
        client = Client.objects.get(user=request.user)
        instance.client = client
        db_bank_account = check_db_bank_account(client=client)
        if db_bank_account == False:
            form.save()
        pay = pay_subsctiption(request=request,client=client)
        if pay == True:
            return redirect('/weather')
    form = BankForm()  
    context = {'form' : form}
    return render(request,'weather/subscription_page.html',context)





def no_subscription(request):
    context = {}
    return render(request,'weather/no_subscription.html',context)

