import os
import json
import zipfile
from bs4 import BeautifulSoup

data = list()
age_max = 0
age_min = 99999999
age_avg = 0
age_sum = 0

counter = 0
freq = {}

with zipfile.ZipFile("zip_var_16.zip", "r") as file:
    files = file.namelist()
    for filename in files:
        with file.open(filename) as page:
            soup = BeautifulSoup(page, 'xml')
            
            name = soup.find_all("name")[0].get_text().strip()
            constellation = soup.find_all("constellation")[0].get_text().strip()
            
            spectral_class = soup.find_all("spectral-class")[0].get_text().strip()
            freq[spectral_class] = freq.get(spectral_class, 0) + 1
            
            radius = float(soup.find_all("radius")[0].get_text().strip())
            rotation = float(soup.find_all("rotation")[0].get_text().replace("days", "").strip())
            
            age = float(soup.find_all("age")[0].get_text().replace("billion years", "").strip())
            if age >= age_max:
                age_max = age
            if age <= age_min:
                age_min = age
            age_sum += age
            counter+=1
            
            distance = float(soup.find_all("distance")[0].get_text().replace("million km", "").strip())
            absolute_magnitude = float(soup.find_all("absolute-magnitude")[0].get_text().replace("million km", "").strip())
            
        
        
            star = {
                "Name": name,
                "Constellation": constellation,
                "Spectral_class": spectral_class,
                "Radius": radius,
                "Rotation": rotation,
                "Age": age,
                "Distance": distance,
                "Absolute_magnitude": absolute_magnitude
            }
            data.append(star)


with open("t3_result.json", "w") as file:
    file.write(json.dumps(data, indent=2, ensure_ascii=False))
    
sorted_data = sorted(data, key=lambda x: x["Radius"])
filtered_data = list(filter(lambda x: x["Age"] >= 2, data))

with open("t3_result_sorted.json", "w") as file:
    file.write(json.dumps(sorted_data, indent=2, ensure_ascii=False))

with open("t3_result_filtered.json", "w") as file:
    file.write(json.dumps(filtered_data, indent=2, ensure_ascii=False))

age_avg = age_sum / counter

with open("t3_stats.json", "w") as file:
    file.write(json.dumps(
            {
                "Sum": age_sum,
                "min": age_min,
                "max": age_max,
                "average": age_avg
            },
            indent=2))
    
freq_sorted = dict(sorted(freq.items(), key=lambda x: x[1], reverse=True))

with open("t3_freq.json", "w", encoding="utf-8") as file:
    file.write(json.dumps(freq_sorted, ensure_ascii=False, indent=2))
