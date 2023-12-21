import msgpack
from pymongo import MongoClient

def get_collection(conUrl):
    client = MongoClient(conUrl)
    db = client["task1"]
    return db.person_data

with open("task_3_item.msgpack", "rb") as data_file:
    byte_data = data_file.read()
data = msgpack.unpackb(byte_data)

collection = get_collection("mongodb://localhost:27017")
collection.insert_many(data)

query = {"$or": [{"salary": {"$lt": 25000}},{"salary": {"$gt": 175000}}]}
collection.delete_many(query)

collection.update_many({}, {"$inc": {"age": 1}})

collection.update_many({"job": {"$in": ["Повар"]}},{"$mul": {"salary": 1.05}})

collection.update_many({"city": {"$in": ["Тбилиси"]}},{"$mul": {"salary": 1.07}})

collection.update_many({"$and": [{"city": {"$in": ["Москва"]}},{"job": {"$in": ["Учитель"]}}]},{"$mul": {"salary": 1.10}})

collection.delete_many({"job": "IT-специалист"})
