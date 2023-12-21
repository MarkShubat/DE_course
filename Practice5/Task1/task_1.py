from pymongo import MongoClient
import json


def get_collection(conUrl):
    client = MongoClient(conUrl)
    db = client["task1"]
    return db.person_data


def load_data(fileName):
    with open(fileName, "r", encoding="utf-8") as file:
       lines = file.readlines()
    data = []
    obj = {}
    for line in lines:
        if line.strip() != "=====":
            s = line.strip().split("::")
            obj[s[0]] = int(s[1]) if s[1].isdigit() else s[1]
        else:
            data.append(obj)
            obj = {}
    return data

data = load_data("task_1_item.text")
collection = get_collection("mongodb://localhost:27017")

if collection.count_documents({}) == 0:
    collection.insert_many(data)

persons = list(collection.find({}).limit(10).sort({"salary": -1}))
with open("t1_res_sorted_salary.json", "w", encoding="utf-8") as file:
    file.write(json.dumps(persons, ensure_ascii=False, default=str))

persons = list(collection.find({"age": {"$lt": 45}}, limit=15).sort({"salary": -1}))
with open("t1_res_filtered_age.json", "w", encoding="utf-8") as file:
    file.write(json.dumps(persons, ensure_ascii=False, default=str))

query = {"city": "Куэнка", "job": {"$in": ["Учитель", "Повар", "Психолог"]}}
persons = list(collection.find(query, limit=10).sort({"age": 1}))
with open("t1_res_filtered_city.json", "w", encoding="utf-8") as file:
    file.write(json.dumps(persons, ensure_ascii=False, default=str))

query = {
        "age": {"$gt": 30, "$lt": 45},
        "year": {"$in": [2019, 2020, 2021, 2022]},
        "$or": [{"salary": {"$gt": 50000, "$lte": 75000}},
                {"salary": {"$gt": 125000, "$lt": 150000}}]
    }
with open("t1_res_complex_filter.json", "w", encoding="utf-8") as file:
    file.write(json.dumps(len(list(collection.find(query))), ensure_ascii=False, default=str))
