from lxml import html
import requests
from pprint import pprint

url = 'https://lenta.ru/'

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                         '(KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36'}

response = requests.get(url, headers=headers)

dom = html.fromstring(response.text)

drones = []

items = dom.xpath("//div[@class='card-big _topnews _news'] | //a[@class='card-mini _topnews']")
print(len(items))
for item in items:
    drone = {}
    name = item.xpath(".//text()")
    link = item.xpath("./@href")
    time = item.xpath(".//time/text()")
    data = f"{'-'.join(link[0].split('/')[2:5])} {time[0]}"

    drone['name'] = name[0]
    drone['link'] = f"{url}{link[0]}"
    drone['data'] = data
    drone['source'] = "lenta.ru"

    drones.append(drone)

pprint(drones)
