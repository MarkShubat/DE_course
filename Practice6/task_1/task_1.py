import sys
import os
import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from tqdm import tqdm
import numpy as np



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

file_size = os.path.getsize("H:/data/[1]game_logs.csv")
df = pd.read_csv("H:/data/[1]game_logs.csv")
print(f"Size without optimize: {df.memory_usage(deep=True).sum() // (1024 * 1024)} MB")
df_info(df, file_size, "memory_usage_no_optimize.json")

df_optimize = optimize_df(df)
print(f"Size with optimize: {df_optimize.memory_usage(deep=True).sum() // (1024 * 1024)} MB")
df_info(df_optimize, file_size, "memory_usage_optimize.json")

columns = ["date", "number_of_game", "day_of_week", "park_id","v_manager_name", "length_minutes", "v_hits","h_hits", "h_walks", "h_errors"]
df_optimize_dtype = save_df(df_optimize, columns, "df_optimize_dtype.json")

flag_header = True
size = 0
with open("df_optimize_dtype.json", mode='r') as f:
        dtypes = json.load(f)
        
for elem in pd.read_csv("H:/data/[1]game_logs.csv", usecols=lambda x: x in dtypes.keys(), dtype=dtypes,chunksize=500_000):
    size += elem.memory_usage(deep=True).sum()
    elem.dropna().to_csv("df_filtered.csv", mode="a", header=flag_header, index=False)
    flag_header = False

for key in dtypes.keys():
    if dtypes[key] == 'category':
        dtypes[key] = pd.CategoricalDtype
    else:
        dtypes[key] = np.dtype(dtypes[key])


df_filtered = pd.read_csv("df_filtered.csv", usecols=lambda x: x in dtypes.keys(),dtype=dtypes)
    
histogram(df_filtered, "day_of_week")
pie(df_filtered, "number_of_game")
linear_graphics(df_filtered, "day_of_week", "length_minutes")
box(df_filtered, "number_of_game", "h_errors")
correlation(df_filtered, ["v_hits", "h_hits", "h_walks", "h_errors"])
    
