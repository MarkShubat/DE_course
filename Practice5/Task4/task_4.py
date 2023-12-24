from pymongo import MongoClient
import json
import os
import json
import csv
import msgpack
import pandas as pd


def connect():
    client = MongoClient("mongodb://localhost:27017/")
    collection = client.univercity_db
    return collection.univercity

def insert(collection, data):
    collection.insert_many(data)

def csv_data():
    df = pd.read_csv('cwurData.csv')
    data = df.to_dict(orient='records')
    return data

def data_from_json():
    with open("data.json", 'r', encoding='utf-8') as file:
        items = json.load(file)
    return items

def sort_by_national_rank(collection, limit=10):
    results = []
    for data in collection.find({}, limit=limit).sort({"national_rank": 1}):
        data["_id"] = str(data["_id"])
        results.append(data)
    save_json(sort_by_national_rank.__name__, results)

def filter_by_score_sorted_by_patents(collection):
    results = []
    for data in collection.find({"score": {"$gt": 44.51, "$lt": 44.54}}, limit=15).sort({"patents": -1}):
        data['_id'] = str(data['_id'])
        results.append(data)
    save_json(filter_by_score_sorted_by_patents.__name__, results)

def filter_by_country_sorted_by_citations(collection):
    results = []
    for data in collection.find({"country": {"$in": ["USA"]}}, limit=15).sort({"citations": 1}):
        data['_id'] = str(data['_id'])
        results.append(data)
    save_json(filter_by_country_sorted_by_citations.__name__, results)

def filter_by_country_sorted_by_institution(collection):
    results = []
    for data in collection.find({"country": "Italy", }, limit=10).sort({"institution": 1}):
        data['_id'] = str(data['_id'])
        results.append(data)
    save_json(filter_by_country_sorted_by_institution.__name__, results)

def count_docs(collection):
    results = {"count": collection.count_documents({"$or": [{"influence": {"$gt": 600, "$lte": 800}},{"citations": {"$gt": 500, "$lt": 700}}]})}
    save_json(count_docs.__name__, results)

def count_by_country(collection):
    results = []
    for stat in collection.aggregate([{"$group": {"_id": "$country","count": {"$sum": 1}}},{"$sort": {"count": -1}}]):
        results.append(stat)
    save_json(count_by_country.__name__, results)

def stat_score(collection):
    query = [{"$group": {
        "_id": "result",
        "max": {"$max": "$score"},
        "avg": {"$avg": "$score"},
        "min": {"$min": "$score"}}}]
    results = []
    for stat in collection.aggregate(query):
        results.append(stat)
    save_json(stat_score.__name__, results)

def stat_max_influence_by_min_citations(collection):
    results = []
    for stat in collection.aggregate([{"$sort": {'influence': 1, "citations": -1}},{"$limit": 1}]):
        stat['_id'] = str(stat['_id'])
        results.append(stat)
    save_json(stat_max_influence_by_min_citations.__name__, results)

def stat_publications(collection):
    query = [
            {"$match": {'country': {'$in': ["USA", "Italy"]}}},
            {
                "$group": {
                "_id": "$institution",
                "max": {"$max": "$publications"},
                "avg": {"$avg": "$publications"},
                "min": {"$min": "$publications"}},
            },
            {"$sort": {"_id": -1}},
        ]
    results = []
    for stat in collection.aggregate(query):
        results.append(stat)
    save_json(stat_publications.__name__, results)

def stat_patents(collection):
    query =  [
            {
                "$match":
                {
                    'country': {'$in': ['Australia', "Russia"]},
                    '$or': [{'influence': {"$gt": 400, "$lt": 500}}, {'citations': {"$gt": 600, "$lt": 700}}]
                }
            },
            {
                "$group": 
                {
                    "_id": "result",
                    "max": {"$max": "$patents"},
                    "avg": {"$avg": "$patents"},
                    "min": {"$min": "$patents"}
                }
            }
        ]
    results = []
    for stat in collection.aggregate(query):
        results.append(stat)
    save_json(stat_patents.__name__, results)

def delete(collection):
    print(collection.delete_many({"$or":[{"quality_of_education": {"$lt": 250}},{"quality_of_edcation": {'$gt': 300}}]}))

def delete_filter(collection):
    filter = {
        'country': {'$in': ['USA', "Australia"]},
        '$or': [{'influence': {"$gt": 400, "$lt": 500}}, {'citations': {"$gt": 600, "$lt": 700}}]
    }
    print(collection.delete_many(filter))

def add(collection):
    print(collection.update_many({}, {"$set": {"new_column": 0}}))

def update(collection):
    print(collection.update_many({"country": "USA"}, {"$inc": {"new_column": 1}}))

def update_filter(collection):
    filter = {
        "country": {'$in': ['USA', "Russia", "Italy"]},
        "influence": {"$gt": 400, "$lt": 500}
    }
    update = {"$inc": {"new_column": 2}}
    print(collection.update_many(filter, update))

def save_json(name, data):
    path = ""
    path += str(name) + ".json"
    with open(path, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False)

        
collection = connect()

data1 = csv_data()
data2 = data_from_json()
#insert(collection, data1)
#insert(collection, data2)

sort_by_national_rank(collection)   

filter_by_score_sorted_by_patents(collection)

filter_by_country_sorted_by_citations(collection)

filter_by_country_sorted_by_institution(collection)

count_docs(collection)

count_by_country(collection)

stat_patents(collection)
stat_score(collection)

stat_max_influence_by_min_citations(collection)

stat_publications(collection)

delete(collection)

delete_filter(collection)

add(collection)

update(collection)

update_filter(collection)
