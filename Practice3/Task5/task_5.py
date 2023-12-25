import json
import zipfile
import os
import urllib.request
from bs4 import BeautifulSoup

data = list()
price_max = 0
price_min = 999999999
price_avg = 0
price_sum = 0

counter = 0
freq = {}

url = "https://xn--80aacd1dd1a.xn--p1ai/cars?page="

for i in range(5):
  html_content = urllib.request.urlopen(url + str(i+1)).read() 

  soup = BeautifulSoup(html_content, "html.parser")
  
  items = soup.find_all("div", attrs={"class": "category-list__item"})
            
  for item in items:
    href = item.find_all("a", attrs={"car-card"})[0]["href"]
    name = item.find_all("p", attrs={"car-card__title"})[0].get_text().strip()
    if len(item.find_all("div", attrs={"car-card__params"})[0].get_text().split(", \n        ")) > 1:
      year = item.find_all("div", attrs={"car-card__params"})[0].get_text().split(", \n        ")[0].replace("год", "").strip()
      mileage = item.find_all("div", attrs={"car-card__params"})[0].get_text().split(", \n        ")[1].replace("км", "").strip()
    else:
      year = item.find_all("div", attrs={"car-card__params"})[0].get_text().replace("год", "").strip()
      mileage = "0"
    splitter = "\xa0·\n       \n        "
    
    e_type = item.find_all("div", attrs={"car-card__params"})[1].get_text().split(splitter)[0].strip()
    
    e_drive = item.find_all("div", attrs={"car-card__params"})[1].get_text().split(splitter)[1].strip()
    e_fuel = item.find_all("div", attrs={"car-card__params"})[1].get_text().split(splitter)[2].strip()
    e_volume = item.find_all("div", attrs={"car-card__params"})[1].get_text().split(splitter)[3].strip().replace("\xa0", "").replace("л.","").strip()
    e_power = item.find_all("div", attrs={"car-card__params"})[1].get_text().split(splitter)[4].strip().replace("\xa0", "").replace("л.с.","").strip()

    price = float(item.find_all("div", attrs={"car-card__price-actual"})[0].get_text().replace("₽", "").replace(",","").strip())
    
        
    car = {
        "Href": href,
        "Name": name,
        "Price": price,
        "Year": year,
        "Mileage": mileage,
        "Engine type": e_type,
        "Drive" : e_drive,
        "Fuel": e_fuel,
        "Volume, L": e_volume,
        "Power, H.P.": e_power
        }
    data.append(car)
            
for elem in data:
    price = data["Price"]
    if price >= price_max:
      price_max = price
    if price <= price_min:
      price_min = price
    price_sum += price
    counter+=1

    e_type = elem["Engine type"]
    freq[e_type] = freq.get(e_type, 0) + 1    
    
with open("t5_result.json", "w") as file:
    file.write(json.dumps(data, indent=2, ensure_ascii=False))
    
sorted_data = sorted(data, key=lambda x: x["Year"])
filtered_data = list(filter(lambda x: x["Price"] >= 1000000, data))

with open("t5_result_sorted.json", "w") as file:
    file.write(json.dumps(sorted_data, indent=2, ensure_ascii=False))

with open("t5_result_filtered.json", "w") as file:
    file.write(json.dumps(filtered_data, indent=2, ensure_ascii=False))

price_avg = price_sum / counter

with open("t5_stats.json", "w") as file:
    file.write(json.dumps(
            {
                "Sum": price_sum,
                "min": price_min,
                "max": price_max,
                "average": price_avg
            },
            indent=2))
    
freq_sorted = dict(sorted(freq.items(), key=lambda x: x[1], reverse=True))

with open("t5_freq.json", "w", encoding="utf-8") as file:
    file.write(json.dumps(freq_sorted, ensure_ascii=False, indent=2))
