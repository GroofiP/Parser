# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class LabirintsItem(scrapy.Item):
    _id = scrapy.Field()
    authors = scrapy.Field()
    name = scrapy.Field()
    rating = scrapy.Field()
    price = scrapy.Field()
    sale = scrapy.Field()
    url = scrapy.Field()
