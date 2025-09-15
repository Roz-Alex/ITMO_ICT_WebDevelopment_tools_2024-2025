import re
from datetime import datetime, timedelta

from bs4 import BeautifulSoup
import requests

from lab_2.task2.common.db import save_car
from lab_2.task2.common.connection import init_db, engine



def parse_car(car):
    try:

        s = car.find("div", "ListingItemUniversalPrice__title-Mi4tV").contents[0].contents[0].strip()
        price = int(re.sub(r'[^\d]', '', s))
        info_list = \
        car.find("a", "Link ListingItemTitle__link ListingItemUniversalSpecs__link-vOcwF").contents[0].split(',')

        car_name, year, mileage = (info_list + ["0"] * 3)[:3]

        car_name = re.sub(r'[^a-zA-Zа-яА-ЯёЁ0-9 .,]', '', car_name)
        year = re.sub(r'[^\d]', '', year)
        mileage = int(re.sub(r'[^\d]', '', mileage))

        lst = car.find_all("span", "ListingItemUniversalSpecs__spec-IcgjK")

        specs = ''
        for l in lst:
            specs += re.sub(r'[^a-zA-Zа-яА-ЯёЁ0-9 .,]', '', l.contents[0])
            specs += ' '

        data = {
            "name": car_name,
            "year": year,
            "price": price,
            "specs": specs,
            "mileage": mileage,
        }
        return data

    except Exception as e:
        print(f"[ERROR] Ошибка при парсинге карточки: {e}")
        return None


def process_page(html):
    soup = BeautifulSoup(html, "html.parser")
    cars = soup.find_all("div", "ListingCars__universalSnippetWrapper")

    for car in cars:
        data = parse_car(car)
        if data:
            save_car(data)


if __name__ == "__main__":

    #init_db()

    process_page(requests.get(url).content)
