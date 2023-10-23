import csv
from bs4 import BeautifulSoup
with open("text_5_var_16") as file1:
    with open("t5_result",'w') as file2:
        soup = BeautifulSoup(file1, "html.parser")
        result = soup.find_all('tr')
        for elem in result:
            row = list(filter(lambda x: x != "", elem.text.split('\n')))
            csv.writer(file2).writerow(row)


