with open("text_2_var_16") as file:
    text = file.readlines()
result = []
for line in text:
    summ = 0
    line = line.split(",")
    for elem in line:
        summ += int(elem)
    result.append(summ)
file = open('t2_result.txt', 'w')
for elem in result:
  file.write(str(elem) + "\n")
file.close()
