with open("text_1_var_16") as file:
    text = file.readlines()
result = {}
separators = [".", ",", "!", "?",":",";"]
for line in text:
    for s in separators:
        line = line.replace(s," ")
    line = line.split()
    for elem in line:
        if elem in result:
            result[elem] += 1
        else:
            result[elem] = 1
result = sorted(result.items(), key=lambda item: item[1], reverse=True)
file = open('t1_result.txt', 'w')
for key, value in result:
  file.write(f'{key}:{value}\n')
file.close()
