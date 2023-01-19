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
            if (city,latitude, longitude) in city_list:
                continue
            city_list.append((city,latitude, longitude))
        except:
            continue
    return city_list

def add_city(city_list):
    for city in city_list:
        city_name = city[0]
        city_latitude = city[1]
        city_longitude = city[2]
        try:
            c= City.objects.get(name=city_name)
        except:
            c = City(name=city_name, latitude=city_latitude, longitude=city_longitude)
            #c.name = currency_name
            c.save()  #To test out the code, replace this by print(c)