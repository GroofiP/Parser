import time
from pprint import pprint

from pymongo import MongoClient
from selenium import webdriver
from selenium.common.exceptions import ElementNotInteractableException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

client = MongoClient("127.0.0.1", 27017)["Mvideo"]
mvideo = client.mvideo

driver = webdriver.Firefox()

driver.get('https://www.mvideo.ru/')

elem = driver.find_element(By.CLASS_NAME, "text")

for _ in range(3):
    elem.send_keys(Keys.PAGE_DOWN)

time.sleep(5)

button = driver.find_element(By.XPATH, "//button[@class='tab-button ng-star-inserted']")
button.click()
elem = driver.find_element(By.XPATH, "//mvid-carousel[@class='carusel ng-star-inserted']//mvid-product-cards-group")
items_name = elem.find_elements(By.XPATH, "./div[@class='product-mini-card__name ng-star-inserted']")
items_price = elem.find_elements(By.XPATH, "./div[@class='product-mini-card__price ng-star-inserted']")
items_rating = elem.find_elements(By.XPATH, "./div[@class='product-mini-card__rating ng-star-inserted']")


for _ in range(0, len(items_name) - 1):
    name = items_name[_].find_element(By.XPATH, "./div/a/div").text
    link = items_name[_].find_element(By.XPATH, ".//a").get_attribute("href")
    price = items_price[_].find_element(By.CLASS_NAME, "price__main-value").text
    rating = items_rating[_].find_element(By.CLASS_NAME, "value").text
    mvideo.insert_one({"name": name, "link": link, "price": price, "rating": rating})

for doc in mvideo.find():
    print(doc)
