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
            latitude = float(f"{detail[1].get_text().strip()}.{detail[2].get_text().strip()}")
            longitude = float(f"{detail[3].get_text().strip()}.{detail[4].get_text().strip()}")
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


def get_ticket(city_from, state_from, city_to, state_to, date):
    import requests
    from bs4 import BeautifulSoup

    year = int(date.split("-")[0])
    month = int(date.split("-")[1])
    day = int(date.split("-")[2])

    url = f"https://www.travelmath.com/flying-time/from/{city_from},+{state_from}/to/{city_to},+{state_to}"
    #url = https://www.travelmath.com/flying-time/from/New+York,+NY/to/Boston,+MA

    response = requests.get(url)
    soup = BeautifulSoup(response.content, features="html.parser")
    data_lines = soup.find_all('h3', {"id":"flyingtime"})
    fly_time=data_lines[0].get_text().strip()



    return fly_time
