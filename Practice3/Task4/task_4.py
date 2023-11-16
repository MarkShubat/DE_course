import os
import json
import zipfile
from bs4 import BeautifulSoup

data = list()
price_max = 0
price_min = 99999999
price_avg = 0
price_sum = 0

counter = 0
freq = {}

with zipfile.ZipFile("zip_var_16.zip", "r") as file:
    files = file.namelist()
    for filename in files:
        with file.open(filename) as page:
            soup = BeautifulSoup(page, 'xml')
            
            clothings = soup.find_all("clothing")
            for clothing in clothings:
                item = {}
                for elem in clothing.contents:
                    if elem.name is not None:
                        try:
                            item[elem.name] = float(elem.get_text().strip())
                            if elem.name == "price":
                                price = float(elem.get_text().strip())
                                if price >= price_max:
                                    price_max = price
                                if price <= price_min:
                                    price_min = price
                                price_sum += price
                                counter += 1
                        except:
                            item[elem.name] = elem.get_text().strip()
                            if elem.name == "category":
                                freq[elem.get_text().strip()] = freq.get(elem.get_text().strip(), 0) + 1
                data.append(item)
            
with open("t4_result.json", "w") as file:
    file.write(json.dumps(data, indent=2, ensure_ascii=False))
    
sorted_data = sorted(data, key=lambda x: x["rating"])
filtered_data = list(filter(lambda x: x["price"] >= 700000, data))

with open("t4_result_sorted.json", "w") as file:
    file.write(json.dumps(sorted_data, indent=2, ensure_ascii=False))

with open("t4_result_filtered.json", "w") as file:
    file.write(json.dumps(filtered_data, indent=2, ensure_ascii=False))

price_avg = price_sum / counter

with open("t4_stats.json", "w") as file:
    file.write(json.dumps(
            {
                "Sum": price_sum,
                "min": price_min,
                "max": price_max,
                "average": price_avg
            },
            indent=2))
    
freq_sorted = dict(sorted(freq.items(), key=lambda x: x[1], reverse=True))

with open("t4_freq.json", "w", encoding="utf-8") as file:
    file.write(json.dumps(freq_sorted, ensure_ascii=False, indent=2))
