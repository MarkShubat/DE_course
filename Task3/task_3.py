VAR = 16
with open("text_3_var_16") as file:
    text = file.readlines()
file = open('t3_result.txt', 'w')
for line in text:    
    line = line.split(",")
    result = ""
    for i in range(len(line)):
        if line[i] == "NA" and i != len(line) - 1 and i != 0:
            line[i] = (int(line[i-1]) + int(line[i + 1])) / 2
        if float(line[i]) ** 0.5 >= VAR + 50:
            result += str(line[i]) + ","
    result.strip(",")
    file.write(result)
file.close()
