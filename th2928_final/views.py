from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse

from th2928_final import support_functions
from th2928_final.models import *

# Create your views here.
def home(request):
    data = {}
    import datetime
    time=datetime.datetime.now()
    data["time_of_day"] = time
    print(time)
    return render(request, "home.html", context= data)

def maintenance(request):
    data = dict()
    try:
        choice = request.GET['selection']
        if choice == "city":
            support_functions.add_city(support_functions.get_city_list())
            c_list = City.objects.all()
            print("Got c_list", len(c_list))
            data['city'] = c_list
            return HttpResponseRedirect(reverse('city'))
    except:
        pass
    return render(request,"maintenance.html",context=data)

def view_cities(request):
    data = dict()
    try:
        choice = request.GET['city.x']
        if choice != None:
            support_functions.add_city(support_functions.get_city_list())
            c_list = City.objects.all()
            print("Got c_list", len(c_list))
            data['city'] = c_list
            return HttpResponseRedirect(reverse('city'))
    except:
        pass

    c_list = City.objects.all()
    data['cities'] = c_list
    return render(request,'cities.html',context=data)

def view_weather(request):
    data = dict()
    try:
        city = request.GET['city']
        c1 = City.objects.get(name=city)
        try:
            user = request.user
            if user.is_authenticated:
                account_holder = AccountHolder.objects.get(user=user)
                account_holder.cities_visited.add(c1)
                data['cities_visited'] = account_holder.cities_visited.all()
        except:
            pass
        support_functions.update_weather(c1)
        data['city'] = c1
        data['cities'] = City.objects.all()
        try:
            weather = Weather.objects.filter(city__name__contains=c1.name)[0].weather
            data['weather'] = weather
        except:
            data['weather'] = "Not Available"
    except:
        pass
    return render(request, "weather.html", data)

def register_new_user(request):
    context = dict()
    form = UserCreationForm(request.POST)
    if form.is_valid():
        new_user = form.save()
        dob = request.POST["dob"]
        acct_holder = AccountHolder(user=new_user,date_of_birth=dob)
        acct_holder.save()
        return render(request,"home.html",context=dict())
    else:
        form = UserCreationForm()
        context['form'] = form
        return render(request, "registration/register.html", context)

def journey(request):
    data = dict()
    try:
        decision = request.GET['decision']
        decision = City.objects.get(name=decision)
        data['decision'] = decision
    except:
        pass
    return render(request, 'journey.html', context=data)

def ticket(request):
    data = dict()

    try:
        decision = request.GET['decision']
        city_from = request.GET['city-from'].replace(" ", "+")
        state_from = request.GET['state-from'].replace(" ", "+")
        city_to = decision.split(", ")[0]
        state_to = decision.split(", ")[1]
        date = request.GET['date']

        price = support_functions.get_ticket(city_from, state_from, city_to, state_to, date)
        data['fare'] = price
        #price = round(price, 2)
        #data['fare']= f'${price}'
    except:
        pass
    return render(request, 'ticket.html', context=data)

def assignment2(request):
    data = dict()
    return render(request, 'assignment2.html', context=data)