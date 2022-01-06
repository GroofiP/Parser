from pymongo import MongoClient

client = MongoClient("127.0.0.1", 27017)["Works"]

works = client.works

price = int(input("Введите ожидаемую зарплату: "))

for doc in works.find({"$or": [{"price.min": {"$gte": price}}, {"price.max": {"$gte": price}}]}):
    print(doc)
