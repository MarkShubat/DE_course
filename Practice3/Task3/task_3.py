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
        data["average_price"] = (data["average_price"] + price) / 2
        data["max_price"] = max(data["max_price"], price)
        data["min_price"] = min(data["min_price"], price)
    else:
        result[name] = {"average_price": price, "max_price": price, "min_price": price}

file = open("t3_result.json", "w")
json.dump([{"name": name, **data} for name, data in result.items()], file, indent=2)
file.close()

file = open("t3_result.msgpack", "wb")
file.write(msgpack.packb(result))
file.close()

print("Размер оригинального файла: " + str(os.path.getsize('t3_result.json')))
print("Размер сжатого файла: " + str(os.path.getsize('t3_result.msgpack')))
