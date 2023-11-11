import csv
VAR = 16
with open('text_4_var_16', 'rt', encoding='utf-8') as file1:
    with open('t4_result', 'w', encoding='utf-8') as file2:
        summ = 0
        count = 0
        result = []
        for elem in csv.reader(file1, delimiter=','):
            summ += int(elem[4].replace("₽",""))
            count += 1
            result.append([elem[i] for i in range(5)])
        avg = summ / count
        result.sort(key = lambda item: item[0])
        for row in result:
            if int(row[4].replace("₽","")) >= avg and int(row[0]) > 25 + (VAR % 10):
                csv.writer(file2).writerow(row)
