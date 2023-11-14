import pickle
import json

file = open("products_16.pkl", "rb")
products_data = pickle.load(file)
file.close()

file = open("price_info_16.json", "r")
new_prices_data = json.load(file)
file.close()   

price_info_dict = {}

for item in new_prices_data:
    price_info_dict[item["name"]] = item

for product in products_data:
    current_price_info = price_info_dict[product["name"]]
    
    method = current_price_info["method"]
    if method == "sum":
        product["price"] = round(product["price"] + current_price_info["param"],2)
    elif method == "sub":
        product["price"] = round(product["price"] - current_price_info["param"],2)
    elif method == "percent+":
        product["price"] = round(product["price"] * (1 + current_price_info["param"]),2)
    elif method == "percent-":
        product["price"] = round(product["price"] * (1 - current_price_info["param"]),2)

file = open("t4_result.pkl", "wb")
pickle.dump(products_data, file)
file.close()
