from pymongo import MongoClient
import json
import csv


def get_collection(conUrl):
    client = MongoClient(conUrl)
    db = client["task1"]
    return db.person_data

def aggregate1(group, aggregate, collection):
    query = \
        [{"$group":
              {"_id": f"${group}",
               "max_salary": {"$max": f"${aggregate}"},
               "min_salary": {"$min": f"${aggregate}"},
               "avg_salary": {"$avg": f"${aggregate}"}
               }
          }]
    return list(collection.aggregate(query))

def aggregate2(group, collection):
    query = [
        {"$match": {"$or": [{"age": {"$gt": 20, "$lte": 30}},
                            {"age": {"$gt": 45, "$lt": 60}}]}},
        {"$group": {"_id": f"${group}",
                    "max_salary": {"$max": "$salary"},
                    "min_salary": {"$min": "$salary"},
                    "avg_salary": {"$avg": "$salary"}}
         },
        {"$sort": {"_id": 1}}
    ]
    return list(collection.aggregate(query))

data = []
with open(file="task_2_item.csv", mode="r", encoding='utf-8') as file:
    line_with_format = file.readline().strip()
    data_format = line_with_format.split(";")
    data_format_len = len(data_format)

    reader = csv.reader(file, delimiter=";", quotechar='"')
    for row in reader:
        if not row:
            continue

        if len(row) != data_format_len:
            raise Exception(f"row (`{row}`) mismatch format (`{data_format}`)")

        data.append({column: data1 for column, data1 in zip(data_format, row)})
        
collection = get_collection("mongodb://localhost:27017")
collection.insert_many(data)

query = [
        {"$group": {"_id": "salary",
                    "max": {"$max": "$salary"},
                    "min": {"$min": "$salary"},
                    "avg": {"$avg": "$salary"}}}
    ]
items = list(collection.aggregate(query))
with open("t2_res_aggregate_salary.json", 'w', encoding="utf-8") as file:
    file.write(json.dumps(items, ensure_ascii=False))

query = [{"$group": {"_id": "$job", "sum": {"$sum": 1}}}]
items = list(collection.aggregate(query))
with open("t2_res_aggregate_job.json", 'w', encoding="utf-8") as file:
    file.write(json.dumps(items, ensure_ascii=False))

items = aggregate1("job", "salary", collection)
with open("t2_res_aggregate_job_salary.json", 'w', encoding="utf-8") as file:
    file.write(json.dumps(items, ensure_ascii=False))

items = aggregate1("city", "salary", collection)
with open("t2_res_aggregate_city_salary.json", 'w', encoding="utf-8") as file:
    file.write(json.dumps(items, ensure_ascii=False))

items = aggregate1("city", "age", collection)
with open("t2_res_aggregate_city_age.json", 'w', encoding="utf-8") as file:
    file.write(json.dumps(items, ensure_ascii=False))

items = aggregate1("job", "age", collection)
with open("t2_res_aggregate_job_age.json", 'w', encoding="utf-8") as file:
    file.write(json.dumps(items, ensure_ascii=False))

query = [
        {"$group": {"_id": "$age",
                    "max_salary": {"$max": "$salary"}}
        },
        {"$sort": {"_id": 1}}]
items = list(collection.aggregate(query))[0]
with open("t2_res_min_age_max_salary.json", 'w', encoding="utf-8") as file:
    file.write(json.dumps(items, ensure_ascii=False))

query = [
        {"$group": {"_id": "$age",
                    "min_salary": {"$min": "$salary"}}
         },
        {"$sort": {"_id": -1}}
    ]
items = list(collection.aggregate(query))[0]
with open("t2_res_max_age_min_salary.json", 'w', encoding="utf-8") as file:
    file.write(json.dumps(items, ensure_ascii=False))

query = [
        {"$match": {"salary": {"$gt": 50000}}},
        {"$group": {"_id": "$city",
                    "max_age": {"$max": "$age"},
                    "min_age": {"$min": "$age"},
                    "avg_age": {"$avg": "$age"}}
         },
        {"$sort": {"_id": 1}}
    ]
items = list(collection.aggregate(query))
with open("t2_res_aggregate_city_salary_filtered.json", 'w', encoding="utf-8") as file:
    file.write(json.dumps(items, ensure_ascii=False))

items = aggregate2("city", collection)
with open("t2_res_aggregate_city_filtered.json", 'w', encoding="utf-8") as file:
    file.write(json.dumps(items, ensure_ascii=False))

items = aggregate2("job", collection)
with open("t2_res_aggregate_job_filtered.json", 'w', encoding="utf-8") as file:
    file.write(json.dumps(items, ensure_ascii=False))

items = aggregate2("age", collection)
with open("t2_res_aggregate_age_filtered.json", 'w', encoding="utf-8") as file:
    file.write(json.dumps(items, ensure_ascii=False))

query = [
        {"$match": {"job": "Повар"}},
        {"$group": {"_id": "$city",
                    "max_salary": {"$max": "$salary"},
                    "min_salary": {"$min": "$salary"},
                    "avg_salary": {"$avg": "$salary"}}
         },
        {"$sort": {"_id": 1}}
    ]
items = list(collection.aggregate(query))
with open("t2_res_salary_city_cooker.json", 'w', encoding="utf-8") as file:
    file.write(json.dumps(items, ensure_ascii=False))
