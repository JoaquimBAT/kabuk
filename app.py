from selenium import (
    webdriver
)
from selenium.webdriver.common.by import (
    By
)
import re
from bs4 import BeautifulSoup
import pandas as pd
import time
from datetime import date
from selenium.webdriver.common.keys import Keys

# OTA Site Information
site_list = [
    # {"url": "https://www.ikyu.com/", "ota_name": "ikyu"},
    {"url": "https://www.jalan.net/", "ota_name": "jalan"},
    {"url": "https://travel.rakuten.co.jp", "ota_name": "rakuten"}
]

# Initialize DataFrame
df = pd.DataFrame(columns=['event_date', 'ota', 'hotel_name', 'location', 'room_type', 'prices'])

# Current date
day_date = date.today()

driver = webdriver.Chrome()


def handle_ikyu(url):
    pass


def handle_jalan(url):
    print("starting Jalan")
    driver.get(url=url)
    time.sleep(2)
    hokkaido_button = driver.find_element(By.CLASS_NAME, 'label--hokkaido')
    hokkaido_button.click()
    time.sleep(2)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    hotels = soup.find_all('ul', class_="rec-content-info")
    for hotel in hotels:
        hotel_info = hotel.find('li', class_="rec-content-info__name")
        hotel_name = hotel_info.string
        hotel_region = hotel.find('li', class_="rec-content-info__area").string
        hotel_price = int(
            re.findall(r'(\d{1,3}(?:,\d{3})*)', hotel.find('p', class_="rec-content-info-price__unit-price").text)[
                1].replace(',', ''))
        hotel_id = hotel_info.contents[0].get('href').lstrip('/')
        try:
            driver.get(url=url + hotel_id + 'room/')
        except:
            continue
        rooms = BeautifulSoup(driver.page_source, 'html.parser')
        room_types = rooms.find_all('td', class_="td01")
        if len(room_types) == 0:
            continue
        for room in room_types:
            df.loc[len(df)] = {'event_date': day_date,
                               'ota': site['ota_name'],
                               'hotel_name': hotel_name,
                               'location': hotel_region,
                               'room_type': room.text,
                               'prices': hotel_price}


def handle_rakuten(url):
    print("starting Rakuten")
    driver.get(url=url)
    time.sleep(3)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    # rakuten
    hotel_elements = soup.find_all('div', class_=re.compile(r"^hotel swiper-slide.*"))
    for hotel in hotel_elements:
        hotel_info = hotel.find('div', class_="main")
        hotel_name = hotel.find('p', class_="name crown").string
        hotel_region = hotel.find('p', class_="area").string
        hotel_price = int(
            re.search(r'(\d{1,3}(?:,\d{3})*)', hotel.find('div', class_="price").text).group(1).replace(',', ''))
        driver.get(url=hotel_info.contents[1].attrs['href'])
        try:
            rooms_button = driver.find_element(By.ID, 'navRoom')
            rooms_button.click()
        except:
            continue
        room_soup = BeautifulSoup(driver.page_source, 'html.parser')
        room_pages = room_soup.find_all('a', class_="plan-pagination__page")
        seen_hrefs = set()
        unique_pages = []
        for element in room_pages:
            href = element.get('href')
            if href is not None and href not in seen_hrefs:
                seen_hrefs.add(href)
                unique_pages.append(element)
        for page in unique_pages:
            room_soup = BeautifulSoup(driver.page_source, 'html.parser')
            room_names = room_soup.find_all('h4', class_="roombox__name")
            for name in room_names:
                df.loc[len(df)] = {'event_date': day_date,
                                   'ota': site['ota_name'],
                                   'hotel_name': hotel_name,
                                   'location': hotel_region,
                                   'room_type': name.string,
                                   'prices': hotel_price}
            url = page.get('href')
            driver.get(url=f"https:{url}")
            time.sleep(1)


# Map ota_name to corresponding functions
function_map = {
    # "ikyu": handle_ikyu,
    "jalan": handle_jalan,
    "rakuten": handle_rakuten
}

for site in site_list:
    # Get the function based on ota_name
    function_to_call = function_map.get(site["ota_name"])

    # Call the function with the corresponding url
    if function_to_call:
        function_to_call(site["url"])
    else:
        print(f"No function found for {site['ota_name']}")

# Save output
df.to_csv('output.csv', index=False)
