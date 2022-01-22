from lxml import html
import requests
from pprint import pprint

from pymongo import MongoClient

url = 'https://lenta.ru/'

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                         '(KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36'}

client = MongoClient("127.0.0.1", 27017)["Lenta"]
lenta = client.lenta

response = requests.get(url, headers=headers)
dom = html.fromstring(response.text)


items = dom.xpath("//div[@class='card-big _topnews _news'] | //a[@class='card-mini _topnews']")
print(len(items))
for number, item in enumerate(items):
    drone = {}
    name = item.xpath(".//text()")
    link = item.xpath("./@href")
    time = item.xpath(".//time/text()")
    data = f"{'-'.join(link[0].split('/')[2:5])} {time[0]}"

    drone['name'] = name[0]
    drone['link'] = f"{url}{link[0]}"
    drone['data'] = data
    drone['source'] = "lenta.ru"

    lenta.insert_one(drone)

for doc in lenta.find():
    print(doc)
