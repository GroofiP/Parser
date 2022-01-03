import json
from pprint import pprint

from bs4 import BeautifulSoup
import requests

# https://spb.hh.ru/search/vacancy?area=2&fromSearchLine=true&text=django
from help import generation_number

URL = "https://spb.hh.ru/"
HEADERS = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) "
                         "Chrome/96.0.4664.110 Safari/537.36"}

additional_url = "search/vacancy"

params = {
    "area": 2,
    "fromSearchLine": "true",
    "text": input("Введите должность: ")
}

power = True
data_jobs = {}
number = generation_number()

responce = requests.get(f"{URL}{additional_url}", headers=HEADERS, params=params)
soup = BeautifulSoup(responce.text, "html.parser")
jobs = soup.find_all("div", {"vacancy-serp-item"})

while power:
    for job in jobs:
        name = job.find("a", {"bloko-link"}).text
        price_text = job.find("span", {"data-qa": "vacancy-serp__vacancy-compensation"})
        if price_text:
            price_text = price_text.text
            prices = price_text.split()
            try:
                if prices[0] == "от":
                    price = {"min": int(f"{prices[1]}{prices[2]}"), "max": None, "currency": prices[3]}
                elif prices[0] == "до":
                    price = {"min": None, "max": int(f"{prices[1]}{prices[2]}"), "currency": prices[3]}
                else:
                    price = {"min": int(f"{prices[0]}{prices[1]}"), "max": int(f"{prices[3]}{prices[4]}"),
                             "currency": prices[5]}
            except ValueError:
                price = {"min": None, "max": None, "currency": None}
        else:
            price = {"min": None, "max": None, "currency": None}
        link = job.find("a", {"bloko-link"}).get("href")
        data_job = {
            "Name": name,
            "Price": price,
            "Link": link,
            "Site": "spb.hh.ru"
        }

        data_jobs.update({f"job_{next(number)}": data_job})

    button_text = soup.find("a", {"data-qa": "pager-next"})
    if button_text:
        additional_url = button_text.get("href")
        responce = requests.get(f"{URL[0:-1]}{additional_url}", headers=HEADERS)
        soup = BeautifulSoup(responce.text, "html.parser")
        jobs = soup.find_all("div", {"vacancy-serp-item"})
    else:
        power=False


pprint(data_jobs)

with open('data_jobs.json', 'w', encoding="UTF-8") as f:
    json.dump(data_jobs, f, indent=4)
