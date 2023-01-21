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
    '''
    import statistics
    import time
    from selenium import webdriver
    from selenium.webdriver import
    from selenium.webdriver.firefox.service import Service
    from selenium.webdriver.common.by import By
    from webdriver_manager.firefox import GeckoDriverManager

    # start by defining the options
    options = webdriver.FirefoxOptions()
    options.headless = True  # it's more scalable to work in headless mode
    # normally, selenium waits for all resources to download
    # we don't need it as the page also populated with the running javascript code.
    options.page_load_strategy = 'none'
    # this returns the path web driver downloaded
    firefox_path = GeckoDriverManager().install()
    firefox_service = Service(firefox_path)
    # pass the defined options and service objects to initialize the web driver
    driver = Firefox(options=options, service=firefox_service)
    driver.implicitly_wait(5)
    '''

    import statistics
    import time
    from selenium import webdriver
    from selenium.webdriver import Chrome
    from selenium.webdriver.chrome.service import Service
    from selenium.webdriver.common.by import By
    from webdriver_manager.chrome import ChromeDriverManager

    # start by defining the options
    options = webdriver.ChromeOptions()
    options.headless = True  # it's more scalable to work in headless mode
    # normally, selenium waits for all resources to download
    # we don't need it as the page also populated with the running javascript code.
    options.page_load_strategy = 'none'
    # this returns the path web driver downloaded
    chrome_path = ChromeDriverManager().install()
    chrome_service = Service(chrome_path)
    # pass the defined options and service objects to initialize the web driver
    driver = Chrome(options=options, service=chrome_service)
    driver.implicitly_wait(5)

    year = int(date.split("-")[0])
    month = int(date.split("-")[1])
    day = int(date.split("-")[2])

    url = f"https://www.cheapoair.com/air/listing?&d1={city_from}+{state_from}&r1={city_to}+{state_to}&dt1={month}/" \
          f"{day}/{year}&triptype=ONEWAYTRIP&cl=ECONOMY&ad=1&se=0&ch=0&infs=0&infl=0"
    #url = f"https://www.cheapoair.com/air/listing?&d1=New+York+NY&r1=Boston+Mass&dt1=2/16/2023&triptype=ONEWAYTRIP&cl=ECONOMY&ad=1&se=0&ch=0&infs=0&infl=0

    ticket_ls = list()
    try:
        driver.get(url)
        time.sleep(15)
    except:
        return ticket_ls
    scraped_ls = [ele.text for ele in driver.find_elements(By.CSS_SELECTOR, "div[class*='fare-details']")]
    print(scraped_ls)
    try:
        for ii in range(15):
            if ii % 2 == 0:
                ticket_ls.append(float(scraped_ls[ii].split("$")[1]))
    except:
        for ii in range(len(scraped_ls)):
            if ii % 2 == 0:
                ticket_ls.append(float(scraped_ls[ii].split("$")[1]))

    return statistics.mean(ticket_ls)
