import json
import zipfile
import os
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
            html_content = page.read()
        soup = BeautifulSoup(html_content, "html.parser")

        items = soup.find_all("div", attrs={"class": "product-item"})
            
        for item in items:
            id = item.a["data-id"]
            href = item.find_all("a")[1]["href"]
            img_src = item.find_all("img")[0]["src"]
            name = item.find_all("span")[0].get_text().strip()
            
            price = int(item.find_all("price")[0].get_text().replace("₽", "").replace(" ", "").strip())
            if price >= price_max:
                price_max = price
            if price <= price_min:
                price_min = price
            price_sum += price
            counter+=1
            
            bonus = item.find_all("strong")[0].get_text().replace("+ начислим", "").replace("бонусов", "").strip()

            info = {}
            props = item.find_all("li")
            for prop in props:
                freq[prop["type"]] = freq.get(prop["type"], 0) + 1    
                info[prop["type"]] = prop.get_text().strip()
        
            product = {
                "Id": id,
                "Href": href,
                "Img_src": img_src,
                "Name": name,
                "Price": price,
                "Bonus": bonus,
                "Info": info,
            }
            data.append(product)


with open("t2_result.json", "w", encoding="utf-8") as file:
    file.write(json.dumps(data, indent=2, ensure_ascii=False))
    
sorted_data = sorted(data, key=lambda x: x["Id"])
filtered_data = list(filter(lambda x: x["Price"] >= 100000, data))

with open("t2_result_sorted.json", "w", encoding="utf-8") as file:
    file.write(json.dumps(sorted_data, indent=2, ensure_ascii=False))

with open("t2_result_filtered.json", "w", encoding="utf-8") as file:
    file.write(json.dumps(filtered_data, indent=2, ensure_ascii=False))

price_avg = price_sum / counter

with open("t2_stats.json", "w", encoding="utf-8") as file:
    file.write(json.dumps(
            {
                "Sum": price_sum,
                "min": price_min,
                "max": price_max,
                "average": price_avg
            },
            indent=2))
    
freq_sorted = dict(sorted(freq.items(), key=lambda x: x[1], reverse=True))

with open("t2_freq.json", "w", encoding="utf-8") as file:
    file.write(json.dumps(freq_sorted, ensure_ascii=False, indent=2))

