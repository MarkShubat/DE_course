import pandas as pd
import msgpack
import json
import os

result = dict()
data = pd.read_csv('titanic.csv')
num = ['Survived', 'Pclass', 'Age', 'Siblings/Spouses Aboard', 'Parents/Children Aboard', 'Fare']
lit = ['Name', 'Sex']

def procNums(result, data, columns):
  for column in columns:
    result[column] = {
      'MAX': data[column].max(),
      'MIN': data[column].min(),
      'AVG': data[column].mean(),
      'SUM': data[column].sum(),
      'STD': data[column].std(),
    }

def procLits(result, data, columns):
  for column in columns:
    result[column] = {
      'FRQ': data[column].value_counts().to_dict()
    }

procNums(result, data, num)
procLits(result, data, lit)

df = pd.DataFrame(result)
df.to_json('t5_result.json')
df.to_csv('t5_result.csv')
df.to_pickle('t5_result.pkl')

file = open('t5_result.msgpack', 'wb')
file.write(msgpack.packb(df.to_dict()))
file.close()

print("Размер json файла: " + str(os.path.getsize('t5_result.json')))
print("Размер csv файла: " + str(os.path.getsize('t5_result.csv')))
print("Размер pkl файла: " + str(os.path.getsize('t5_result.pkl')))
print("Размер msgpack файла: " + str(os.path.getsize('t5_result.msgpack')))
