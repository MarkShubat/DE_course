import json
import msgpack
import os

file = open('products_16.json')
json_data = json.load(file)
file.close()

result = {}
for item in json_data:
    name = item["name"]
    price = item["price"]
    if name in result:
        data = result[name]
        data["count"]+=1
        data["summ"] += price
        data["max_price"] = max(data["max_price"], price)
        data["min_price"] = min(data["min_price"], price)
    else:
        result[name] = {"average_price": price, "max_price": price, "min_price": price, "count": 1, "summ": int(price)}
result1 ={}
for item in result:
    result[item]["average_price"] = result[item]["summ"] / result[item]["count"]
    result1[item] = {"average_price": result[item]["average_price"], "max_price": result[item]["max_price"], "min_price": result[item]["min_price"]}
file = open("t3_result.json", "w")
json.dump([{"name": name, **data} for name, data in result1.items()], file, indent=2)
file.close()

file = open("t3_result.msgpack", "wb")
file.write(msgpack.packb(result1))
file.close()

print("Размер оригинального файла: " + str(os.path.getsize('t3_result.json')))
print("Размер сжатого файла: " + str(os.path.getsize('t3_result.msgpack')))
