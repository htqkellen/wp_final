from th2928_final.models import *


def get_city_list():
    city_list = list()
    import requests
    from bs4 import BeautifulSoup
    url = "https://www.infoplease.com/us/geography/latitude-and-longitude-us-and-canadian-cities"
    response = requests.get(url)
    if not response.status_code == 200:
        return city_list
    soup = BeautifulSoup(response.content, features="html.parser")
    data_lines = soup.find_all('tr')
    for line in data_lines:
        try:
            detail = line.find_all('td')
            city = detail[0].get_text().strip()
            latitude = float(detail[1].get_text().strip())+float(detail[2].get_text().strip())/60
            longitude = float(detail[3].get_text().strip())+float(detail[4].get_text().strip())/60
            if "Can." in city:
                continue
            if (city, latitude, longitude) in city_list:
                continue
            city_list.append((city, latitude, longitude))
        except:
            continue
    return city_list


def add_city(city_list):
    for city in city_list:
        city_name = city[0]
        city_latitude = city[1]
        city_longitude = city[2]
        try:
            c = City.objects.get(name=city_name)
        except:
            c = City(name=city_name, latitude=city_latitude, longitude=city_longitude)
            # c.name = currency_name
            c.save()  # To test out the code, replace this by print(c)


def get_weather(city, lat, long):
    url = f"https://forecast.weather.gov/MapClick.php?lat={lat}&lon={-long}"
    import requests
    from bs4 import BeautifulSoup
    weather_ls = list()
    try:
        page_source = BeautifulSoup(requests.get(url).content, features="html.parser")
    except:
        return weather_ls
    data = page_source.find_all("p", {"class": "short-desc"})
    for line in data:
        try:
            weather = line.get_text(separator=" ").strip()
            weather_ls.append((city, weather))
        except:
            continue
    return weather_ls


def update_weather(city):
    try:
        new_weathers = get_weather(city.name, city.latitude, city.longitude)
        for new_weather in new_weathers:
            from datetime import datetime, timezone
            time_now = datetime.now(timezone.utc)
            try:
                weather_object = Weather.objects.get(city=city)
                weather_object.weather = new_weather[1]
                weather_object.update_date = time_now
            except:
                weather_object = Weather(city=city, weather=new_weather[1],
                                         update_date=time_now)
            weather_object.save()
    except:
        pass


def get_estimate(city_from, state_from, city_to, state_to, date):
    import requests
    from bs4 import BeautifulSoup

    result = []

    year = int(date.split("-")[0])
    month = int(date.split("-")[1])
    day = int(date.split("-")[2])

    url = f"https://www.travelmath.com/flying-time/from/{city_from},+{state_from}/to/{city_to},+{state_to}"
    #url = https://www.travelmath.com/flying-time/from/New+York,+NY/to/Boston,+MA

    response = requests.get(url)
    soup = BeautifulSoup(response.content, features="html.parser")
    data_lines = soup.find_all('h3', {"id":"flyingtime"})
    fly_time=data_lines[0].get_text().strip()
    result.append(fly_time)

    url = f'https://www.travelmath.com/drive-distance/from/{city_from},+{state_from}/to/{city_to},+{state_to}'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, features="html.parser")
    data_lines = soup.find_all('h3', {"id": "drivedist"})
    drive_distance = data_lines[0].get_text().strip()
    result.append(drive_distance)

    url = f'https://www.travelmath.com/cost-of-driving/from/{city_from},+{state_from}/to/{city_to},+{state_to}'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, features="html.parser")
    data_lines = soup.find_all('h3', {"id": "costofdriving"})
    cost = data_lines[0].get_text().strip()
    result.append(cost)


    url = f'https://www.travelmath.com/cities/{city_from},+{state_from}'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, features="html.parser")
    data_lines = soup.find_all('h3', {"class": "space"})
    lat = data_lines[0].get_text().split("/")[0].strip().split(" ")
    long = data_lines[0].get_text().split("/")[1].strip().split(" ")

    lat = float(lat[0][:-1]) + float(lat[1][:-1])/60+float(lat[2][:-1])/3600
    long = float(long[0][:-1]) + float(long[1][:-1]) / 60 + float(long[2][:-1]) / 3600
    result.append([lat,-long])

    return result


def add_markers(m,visiting_cities, my_icon):
    import folium

    lat = City.objects.filter(name=visiting_cities)[0].latitude
    lon = -City.objects.filter(name=visiting_cities)[0].longitude
    if lat != 0.0 and lon != 0.0:
        icon = folium.Icon(color="blue",prefix="fa",icon=my_icon)
        marker = folium.Marker((lat,lon),icon=icon)
        marker.add_to(m)
    return m

def add_markers_mod(m,lat, lon, my_icon):
    import folium
    if lat != 0.0 and lon != 0.0:
        icon = folium.Icon(color="blue",prefix="fa",icon=my_icon)
        marker = folium.Marker((lat,lon),icon=icon)
        marker.add_to(m)
    return m

def get_state():
    url = "https://www.50states.com/abbreviations.htm"
    import requests
    from bs4 import BeautifulSoup
    state_ls = list()
    try:
        page_source = BeautifulSoup(requests.get(url).content)
    except:
        return state_ls
    body = page_source.find('tbody')
    data_lines = body.find_all('tr')
    for line in data_lines:
        data=line.find_all('td')
        try:
            name = data[0].get_text().strip()
            abb = data[1].get_text().strip()
            postal = data[2].get_text().strip()
            state_ls.append((name,abb, postal))
        except:
            continue
    return state_ls

def update_state():
    try:
        new_states = get_state()
        for new_state in new_states:
            try:
                state_object = State.objects.get(name=new_state[0])
                state_object.postal = new_state[1]
                state_object.abb = new_state[2]
            except:
                state_object = State(name=new_state[0], postal=new_state[1], abb=new_state[2])
            state_object.save()
    except:
        pass
