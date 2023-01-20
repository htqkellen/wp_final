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
    url = f"https://www.expedia.com/Flights-Search?leg1=from%3A{city_from}%2C{state_from}%2Cto%3A{city_to}%2C{state_to}" \
          f"departure%3A{month}%2F{day}%2F{year}TANYT&mode=search&options=carrier%3A*%2Ccabinclass%3A%2Cmaxhops%3A1%2" \
          f"Cnopenalty%3AN&pageId=0&passengers=adults%3A1%2Cchildren%3A0%2Cinfantinlap%3AN&trip=oneway"
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