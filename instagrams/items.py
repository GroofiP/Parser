# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class InstagramsItem(scrapy.Item):
    _id = scrapy.Field()
    username = scrapy.Field()
    photo = scrapy.Field()
    follow = scrapy.Field()
