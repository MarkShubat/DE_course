import requests
import json
response = requests.get("https://www.cbr-xml-daily.ru/daily_json.js")
data = json.loads(response.text)

HTML_TEMPLATE = f"""<!doctype html>
<html lang="ru">
<head>
<meta charset="utf-8" />
<title></title>
<link rel="stylesheet" href="style.css" />
</head>
<body>
<p>Курсы валют:</p>
<p>{data['Valute']['GBP']['Name']} = {data['Valute']['GBP']['Value']} Российских рублей</p>
<p>{data['Valute']['USD']['Name']} = {data['Valute']['USD']['Value']} Российских рублей</p>
<p>{data['Valute']['EUR']['Name']} = {data['Valute']['EUR']['Value']} Российских рублей</p>
<p>{data['Valute']['CNY']['Name']} = {data['Valute']['CNY']['Value']} Российских рублей</p>
<p>{data['Valute']['JPY']['Name']} = {data['Valute']['JPY']['Value']} Российских рублей</p>
</body>
</html>
""" 

with open('t6_result.html', 'w', encoding='utf-8') as file:
      file.write(HTML_TEMPLATE)
