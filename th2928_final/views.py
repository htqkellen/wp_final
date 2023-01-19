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
    c_list = City.objects.all()
    data['cities'] = c_list
    return render(request,'cities.html',context=data)