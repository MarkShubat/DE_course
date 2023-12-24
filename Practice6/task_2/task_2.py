#он заходит в очень длинную итерацию, я не знаю что случилось(((

import sys
import os
import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from tqdm import tqdm
import numpy as np
import warnings
warnings.filterwarnings("ignore")

def df_info(df, file_size, file_save):
    memory_usage_stat = df.memory_usage(deep=True)
    total_memory_usage = float(memory_usage_stat.sum())
    columns_stats = {}

    for column in df:
        columns_stats[column] = {
            'total_memory': float(memory_usage_stat[column]) // 1024,
            'memory_space_percentage': round(memory_usage_stat[column] / total_memory_usage * 100, 2),
            'dtype': str(df.dtypes[column])
        }
    
    columns_stats = dict(sorted(list(columns_stats.items()), key=lambda x: x[1]['total_memory'], reverse=True))
    results = {
        'file_size': file_size // 1024, # KB
        'file_in_memory_size': total_memory_usage // 1024, # KB
        'columns_stats': columns_stats
    }
    with open(file_save, "w") as file:
        json.dump(results, file, ensure_ascii=False )
        
    return results

def df_info_chunk(path_to_file, file_save, chunksize=1):
    file_size = os.path.getsize(path_to_file)
    total_memory_usage = 0
    df = pd.read_csv(path_to_file, chunksize=chunksize)  
    columns_stats = {}
    print(df)
    for chunk in tqdm(df):
        print(1)
        chunk_memory_usage_stat = chunk.memory_usage(deep=True)
        total_memory_usage += float(chunk_memory_usage_stat.sum())
        for column in chunk:
            if column in columns_stats:
                columns_stats[column]['total_memory'] += float(chunk_memory_usage_stat[column])
            else:
                columns_stats[column] = {
                    'total_memory': float(chunk_memory_usage_stat[column]),
                    'dtype': str(chunk.dtypes[column])
                }    
    for col in columns_stats.keys():
        columns_stats[col]['memory_space_percentage'] = round(columns_stats[col]['total_memory'] / total_memory_usage * 100, 2)
        columns_stats[col]['total_memory'] = columns_stats[col]['total_memory'] // 1024
    
    columns_stats = dict(sorted(list(columns_stats.items()), key=lambda x: x[1]['total_memory'], reverse=True))
    results = {
        'file_size': file_size // 1024,
        'file_in_memory_size': total_memory_usage // 1024,
        'columns_stats': columns_stats
    }
    
    with open(file_save, "w", encoding='utf-8') as file:
        json.dump(results, file, ensure_ascii=False)

    return results

def optimize_df(df):
    for column in df.select_dtypes(include=['object']):
        len_column = len(df[column])
        len_unique = len(df[column].unique())
        if len_unique / len_column < 0.5:
            df[column] = df[column].astype('category')
            
    for column in df.select_dtypes(include=['int']):
        is_unsigned = False not in set(df[column] >= 0)
        if is_unsigned:
            df[column] = pd.to_numeric(df[column], downcast='unsigned')
        else:
            df[column] = pd.to_numeric(df[column], downcast='signed')
            
    for column in df.select_dtypes(include=['float']):
        df[column] = pd.to_numeric(df[column], downcast='float')
    
    return df

def save_df(df, columns, file_save):
    data = {column_name: df[column_name].dtype.name for column_name in columns}

    with open(file_save, "w", encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False)
        
    return data

def histogram(df, column):
    plt.figure(figsize=(30,15))
    plot = df[column].hist(grid=False, edgecolor='black')
    plt.xlabel(column)
    plot.get_figure().savefig("histogram.jpg")
    plt.close()

def pie(df, column):
    plt.figure()
    groups = df.groupby([column])[column].count()
    circ = groups.plot(kind='pie', y=groups.keys(), autopct='%1.0f%%')
    circ.get_figure().savefig("pie.jpg")
    plt.close()

def linear_graphics(df, group, column):
    plt.figure(figsize=(30,15))
    plt.plot(df.groupby([group])[column].sum().values, marker='*', color='green')
    plt.xlabel(group)
    plt.ylabel(column)
    plt.savefig("linear_graphics.jpg")
    plt.close()

def box(df, c1, c2):
    plt.figure(figsize=(30,15))
    plot = sns.boxplot(data=df, x=c1, y=c2)
    plot.get_figure().savefig("box.jpg")
    plt.close()

def correlation(df, columns):
    data = df.copy()
    plt.figure(figsize=(16,16))
    plot = sns.heatmap(data[columns].corr())
    plot.get_figure().savefig("correlation.jpg")
    plt.close()

file_size = os.path.getsize("H:/data/CIS_Automotive_Kaggle_Sample.csv")
memory_usage = df_info_chunk("H:/data/CIS_Automotive_Kaggle_Sample.csv","memory_usage_no_optimize.json", chunksize=1)
print(f"Size without optimize: {memory_usage['file_in_memory_size']} MB")

dtypes = {'stockNum': pd.StringDtype(),'brandName': pd.CategoricalDtype(),'modelName': pd.CategoricalDtype(),'askPrice': pd.StringDtype(),'isNew': pd.CategoricalDtype(),'color': pd.CategoricalDtype(),'vf_Wheels': pd.StringDtype(),'vf_WheelSizeFront': pd.StringDtype(), 'vf_Windows': pd.StringDtype(),'vf_WheelSizeRear': pd.StringDtype() }

flag_header = True
size = 0
chunk = pd.read_csv("H:/data/CIS_Automotive_Kaggle_Sample.csv", usecols=lambda x: x in dtypes.keys(), dtype=dtypes,chunksize=1)
for elem in tqdm(chunk):
        size += part.memory_usage(deep=True).sum()
        elem.dropna().to_csv("df_filtered.csv", mode="a", header=flag_header, index=False)
        flag_header = False

df = pd.read_csv("df_filtered.csv")
df_optimize = optimize_df(df)
print(f"Memory size dataset with optimize: {df_optimize.memory_usage(deep=True).sum() // (1024**2)} MB")
df_info(df_optimize, file_size, "memory_usage_no_optimize.json")

dtypes = save_df(df_optimize, dtypes.keys(), "df_optimize_dtype.json")
    
for key in dtypes.keys():
    if dtypes[key] == 'category':
        dtypes[key] = pd.CategoricalDtype
    else:
        dtypes[key] = np.dtype(dtypes[key])
print(dtypes)

print(df_optimize.info())
    
histogram(df_optimize, "brandName")
pie(df_optimize, "isNew")
linear_graphics(df_optimize, "brandName", "vf_Windows")
boxplot(df_optimize, "isNew", "askPrice")
correlation(df_optimize, ["askPrice", "vf_Wheels", "vf_WheelSizeFront", "vf_WheelSizeRear", "vf_Windows"])
