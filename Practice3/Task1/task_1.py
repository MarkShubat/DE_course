import json
import zipfile
import os
from bs4 import BeautifulSoup

data = list()
playtime_max = 0
playtime_min = 9999999
playtime_avg = 0
playtime_sum = 0

counter = 0
freq = {}

with zipfile.ZipFile("zip_var_16.zip", "r") as file:
    files = file.namelist()
    for filename in files:
        with file.open(filename) as page:
            html_content = page.read()
        soup = BeautifulSoup(html_content, "html.parser")

        t_type = (
            soup.find("div", class_="chess-wrapper")
            .find_all_next("div")[0]
            .find_next("span")
            .get_text(strip=True)
            .split(": ")[1]
            .strip()
        )
        freq[t_type] = freq.get(t_type, 0) + 1

        t_title = soup.find("h1", class_="title").get_text().replace("Турнир:","").replace("/r/n","").strip()
        t_city = soup.find("p", class_="address-p").get_text().split(":")[1].split()[0].replace("Начало", "").strip()
        t_date = soup.find("p", class_="address-p").get_text().split(":")[2].strip()
        tours = int(soup.find("span", class_="count").get_text().split(":")[1].strip())
        
        time = soup.find("span", class_="year").get_text().split(": ")[1].replace("/r/n","").strip()
        time_amount = int(time.split()[0])
        if(time_amount >= playtime_max):
           playtime_max = time_amount
        if(time_amount <= playtime_min):
           playtime_min = time_amount
        playtime_sum += time_amount
        counter+=1

        acess_rating = (
            soup.find("div", class_="chess-wrapper")
            .find_all_next("div")[2]
            .find_all_next("span")[2]
            .get_text()
            .split(":")[1]
            .strip()
        )

        rating = float(
            soup.find("div", class_="chess-wrapper")
            .find_all_next("div")[4]
            .find_all_next("span")[0]
            .get_text()
            .split(":")[1]
            .strip()
        )

        views = int(
            soup.find("div", class_="chess-wrapper")
            .find_all_next("div")[4]
            .find_all_next("span")[1]
            .get_text()
            .split(":")[1]
            .strip()
        )

        img_src = soup.find("img")["src"]

        tournament = {
            "Type": t_type,
            "Title": t_title,
            "City": t_city,
            "Tours": tours,
            "Date": t_date,
            "Playtime": time,
            "Acess rating": acess_rating,
            "Image": img_src,
            "Rating": rating,
            "Views": views,
        }

        data.append(tournament)


for i in range(100):
    print(data[i])
with open("t1_result.json", "w") as file:
    file.write(json.dumps(data, indent=2, ensure_ascii=False))
    
sorted_data = sorted(data, key=lambda x: x["Rating"])
filtered_data = list(filter(lambda x: x["Type"] == 'Swiss', data))

with open("t1_result_sorted.json", "w") as file:
    file.write(json.dumps(sorted_data, indent=2, ensure_ascii=False))

with open("t1_result_filtered.json", "w") as file:
    file.write(json.dumps(filtered_data, indent=2, ensure_ascii=False))

playtime_avg = playtime_sum / counter

with open("t1_stats.json", "w") as file:
    file.write(json.dumps(
            {
                "Sum": playtime_sum,
                "min": playtime_min,
                "max": playtime_max,
                "average": playtime_avg
            },
            indent=2))
    
freq_sorted = dict(sorted(freq.items(), key=lambda x: x[1], reverse=True))

with open("t1_freq.json", "w", encoding="utf-8") as file:
    file.write(json.dumps(freq_sorted, ensure_ascii=False, indent=2))
