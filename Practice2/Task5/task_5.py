import pandas as pd
import msgpack
import json
import os

result = dict()
data = pd.read_csv('titanic.csv')

dataframe = pd.DataFrame(data)
dataframe.to_json('titanic.json')
dataframe.to_pickle('titanic.pkl')
file = open('titanic.msgpack', 'wb')
file.write(msgpack.packb(dataframe.to_dict()))
file.close()

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
      'FRQ': "Doesn't count for this value"
    }

def procLits(result, data, columns):
  for column in columns:
    result[column] = {
      'MAX': "Doesn't count for this value",
      'MIN': "Doesn't count for this value",
      'AVG': "Doesn't count for this value",
      'SUM': "Doesn't count for this value",
      'STD': "Doesn't count for this value",
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

print("Размер json файла: " + str(os.path.getsize('titanic.json')))
print("Размер csv файла: " + str(os.path.getsize('titanic.csv')))
print("Размер pkl файла: " + str(os.path.getsize('titanic.pkl')))
print("Размер msgpack файла: " + str(os.path.getsize('titanic.msgpack')))
