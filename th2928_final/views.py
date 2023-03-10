from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse

from th2928_final import support_functions
from th2928_final.models import *
import folium as folium

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
            name_ls = [obj.name for obj in c_list]
            one = len(name_ls) // 4
            two = len(name_ls) * 2 // 4
            three = len(name_ls) * 3 // 4
            c1_ls = [City.objects.filter(name=name)[0] for name in name_ls[:one]]
            c2_ls = [City.objects.filter(name=name)[0] for name in name_ls[one:two]]
            c3_ls = [City.objects.filter(name=name)[0] for name in name_ls[two:three]]
            c4_ls = [City.objects.filter(name=name)[0] for name in name_ls[three:]]

            data['city'] = c_list
            data['city1'] = c1_ls
            data['city2'] = c2_ls
            data['city3'] = c3_ls
            data['city4'] = c4_ls
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

        if "sunny" in weather.lower():
            bg_img = "sunny"
        elif "clear" in weather.lower():
            bg_img = "clear"
        elif "rain" in weather.lower():
            bg_img = "rain"
        elif "snow" in weather.lower():
            bg_img = "snow"
        elif "cloudy" in weather.lower():
            bg_img = "cloudy"
        elif data['weather'] == "Not Available":
            bg_img = "unhappy"
        else:
            bg_img = "clear"

        data['bg_img'] = f"th2928_final/{bg_img}.gif"

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

        support_functions.update_state()
        data['state'] = State.objects.all()

    except:
        pass
    return render(request, 'journey.html', context=data)

def estimate(request):
    data = dict()

    try:
        decision = request.GET['decision']
        city_from = request.GET['city-from'].replace(" ", "+")
        state_from = request.GET['state-from'].replace(" ", "+")
        city_to = decision.split(", ")[0]
        state_to = decision.split(", ")[1]
        date = request.GET['date']

        data['from'] = f'{city_from.replace("+", " ")}, {state_from.replace("+", " ")}'
        data['to'] = decision

        result = support_functions.get_estimate(city_from, state_from, city_to, state_to, date)
        data['flytime'] = result[0]
        data['drivedist'] = result[1]
        data['cost'] = result[2]

        lat = result[3][0]
        long = result[3][1]



        m = folium.Map(width=400, height=300)
        m = support_functions.add_markers(m, decision, "plane")
        m = support_functions.add_markers_mod(m, lat,long, "house")
        m = m._repr_html_
        data['m'] = m

        data['decision'] = decision
    except:
        pass
    return render(request, 'estimate.html', context=data)

def end(request):
    data = dict()
    decision = request.GET['decision']
    data['decision'] = decision[:-1]
    return render(request, 'end.html', context=data)

def assignment2(request):
    data = dict()
    return render(request, 'assignment2.html', context=data)