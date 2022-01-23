# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from itemloaders.processors import TakeFirst, MapCompose


def int_price(value):
    value = int(value.split(".")[0])
    return value

def take_id(_id):
    _id = _id.split("/")[-1]
    return _id


class LeroymerlinsItem(scrapy.Item):
    _id = scrapy.Field(output_processor=TakeFirst(), input_processor=MapCompose(take_id))
    name = scrapy.Field(output_processor=TakeFirst())
    price = scrapy.Field(output_processor=TakeFirst(), input_processor=MapCompose(int_price))
    photos = scrapy.Field()
    url = scrapy.Field(output_processor=TakeFirst())
