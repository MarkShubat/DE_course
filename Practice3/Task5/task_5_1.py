import json
import zipfile
import os
import urllib.request
from bs4 import BeautifulSoup

data = list()
mileage_max = 0
mileage_min = 999999999
mileage_avg = 0
mileage_sum = 0

counter = 0
freq = {}

elements = ["4ad233b1-ffcb-4f2f-8ab6-64c20837fc3c", "e9a7d510-40b5-4afd-9216-64e486865d3b", "b57aa1bf-c5fc-45c2-b7b6-073d3cda3fac", "3f613b0d-e0eb-443f-8440-c7601ee99621",
            "b26030bb-481c-47a7-8e84-3564a58565d8", "547de95c-791f-46ac-a5b6-5a9844bf052e", "98b9a685-8f44-45df-999a-008abec35c1d", "d060c075-4af7-4d26-b3f8-4709e050d92d",
            "20f1f6e1-79b3-4512-b0e5-fea186b7be81","e6956697-cf68-4b78-b83d-8fe72262ca3e"]
url = "https://xn--80aacd1dd1a.xn--p1ai/cars/"

for el in elements:
  html_content = urllib.request.urlopen(url + el).read() 

  soup = BeautifulSoup(html_content, "html.parser")
  
  items = soup.find_all("h1", attrs={"h1 product-page__title--mobile"})        
  for item in items:
    name = item.get_text().split(",")[0].strip()
    #print(name)
    year = int(soup.find_all("span", attrs={"product-parameters__value"})[0].get_text().strip())
    #print(year)
    mileage = int(soup.find_all("span", attrs={"product-parameters__value"})[1].get_text().strip().replace(" ","").replace("\xa0", "").replace("км",""))
    #print(mileage)
    car_type = soup.find_all("span", attrs={"product-parameters__value"})[2].get_text().strip()
    #print(car_type)
    engine = soup.find_all("span", attrs={"product-parameters__value"})[3].get_text().strip().split()
    
    e_volume = float(engine[0])
    #print(e_volume)
    e_power = float(engine[3])
    #print(e_power)
    e_fuel = engine[6]
    #print(e_fuel)
    
    e_type = soup.find_all("span", attrs={"product-parameters__value"})[4].get_text().strip()
    #print(e_type)
    e_drive = soup.find_all("span", attrs={"product-parameters__value"})[5].get_text().strip()
    #print(e_drive)

    freq[e_type] = freq.get(e_type, 0) + 1
    
    if mileage >= mileage_max:
      mileage_max = mileage
    if mileage <= mileage_min:
      mileage_min = mileage
    mileage_sum += mileage
    counter+=1
        
    car = {
        "Name": name,
        "Year": year,
        "Mileage": mileage,
        "Engine type": e_type,
        "Drive" : e_drive,
        "Fuel": e_fuel,
        "Volume, L": e_volume,
        "Power, H.P.": e_power
        }
    data.append(car)
    #print(car)       

with open("t5_1_result.json", "w") as file:
    file.write(json.dumps(data, indent=2, ensure_ascii=False))
    
sorted_data = sorted(data, key=lambda x: x["Year"])
filtered_data = list(filter(lambda x: x["Mileage"] >= 100000, data))

with open("t5_1_result_sorted.json", "w") as file:
    file.write(json.dumps(sorted_data, indent=2, ensure_ascii=False))

with open("t5_1_result_filtered.json", "w") as file:
    file.write(json.dumps(filtered_data, indent=2, ensure_ascii=False))

mileage_avg = mileage_sum / counter

with open("t5_1_stats.json", "w") as file:
    file.write(json.dumps(
            {
                "Sum": mileage_sum,
                "min": mileage_min,
                "max": mileage_max,
                "average": mileage_avg
            },
            indent=2))
    
freq_sorted = dict(sorted(freq.items(), key=lambda x: x[1], reverse=True))

with open("t5_1_freq.json", "w", encoding="utf-8") as file:
    file.write(json.dumps(freq_sorted, ensure_ascii=False, indent=2))
