# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pymongo import MongoClient


class LabirintsPipeline:
    def __init__(self):
        client = MongoClient('127.0.0.1', 27017)
        self.mongo_base = client.books

    def process_item(self, item, spider):
        item["_id"] = self.get_id(item.get("url"))
        item["authors"] = self.get_authors(item.get("authors"))
        item["sale"] = self.get_sale(item.get("price"), item.get("sale"))
        collection = self.mongo_base[spider.name]
        collection.insert_one(item)

        return item

    def get_id(self, _id):
        list_id = _id.split("/")
        return list_id[-2]

    def get_authors(self, authors):
        return " ,".join(authors)

    def get_sale(self, price, sale):
        if sale:
            discount_calculation = int(price) // 100 * int(sale)
            return price - discount_calculation
        else:
            return "Скидки нет"
