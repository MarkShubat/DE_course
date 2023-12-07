import os
import sqlite3
import json
import csv

dbPath = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "db/DB2")

def connect(path):
    connection = sqlite3.connect(path)
    connection.row_factory = sqlite3.Row
    return connection


def drop_table(connection):
    connection.execute('''DROP TABLE IF EXISTS table1; ''')
    
def create_table(connection):
    connection.execute('''
CREATE TABLE table1 (
    id          INTEGER    PRIMARY KEY AUTOINCREMENT
                           NOT NULL
                           UNIQUE,
    artist      TEXT (256) NOT NULL,
    song        TEXT (256) NOT NULL,
    duration_ms INTEGER    NOT NULL,
    year        INTEGER    NOT NULL,
    tempo       REAL       NOT NULL,
    genre       TEXT (256) NOT NULL,
    loudness    REAL       NOT NULL
);
''')
    
def insert_data(connection, data):
    cursor = connection.cursor()
    cursor.executemany(
        """
        INSERT INTO table1 (artist, song, duration_ms, year, tempo, genre, loudness) 
        VALUES(:artist, :song, :duration_ms, :year, :tempo, :genre, :loudness)
        """, data
    )
    connection.commit()
    cursor.close()

def top_views(connection, top=11):
    cursor = connection.cursor()
    res = cursor.execute(
        '''
        SELECT * 
        FROM table1 
        ORDER BY year DESC LIMIT ?
        ''', [top]
    )
    
    items = []
    for row in res.fetchall():
        items.append(dict(row))
    cursor.close()
    
    return items

def stat_loudness(connection):
    cursor = connection.cursor()
    res = cursor.execute(
        '''
        SELECT 
            SUM(table1.loudness) as sum,
            AVG(table1.loudness) as avg,
            MIN(table1.loudness) as min, 
            MAX(table1.loudness) as max
        FROM table1
        '''
    )
    res = dict(res.fetchone())
    cursor.close()
    return res

def compute_freq_genre(connection):
    cursor = connection.cursor()
    res = cursor.execute(
        '''
        SELECT 
            CAST(COUNT(*) as REAL) / (SELECT COUNT(*) FROM table1) as count,
            genre
        FROM table1
        GROUP BY genre
        '''
    )

    stat_freq = []
    for row in res.fetchall():
        stat_freq.append(dict(row))

    cursor.close()
    return stat_freq

def top_predicate_views(connection, min_tempo=95, top=16):
    cursor = connection.cursor()
    res = cursor.execute(
        '''
        SELECT * 
        FROM table1 
        WHERE tempo >= ?
        ORDER BY year DESC LIMIT ?
        ''', [min_tempo, top]
    )
    
    items = []
    for row in res.fetchall():
        items.append(dict(row))
    cursor.close()
    
    return items

connection = connect(dbPath)

data1 = []
with open("task_3_var_16_part_2.text", 'r', encoding='utf-8') as file:
    data = file.readlines()
    item = dict()
    for i in data:
        if i == '=====\n':
            data1.append(item)
            item = dict()
        else:
            i = i.strip()
            splitted = i.split('::')
            if splitted[0] == 'duration_ms' or splitted[0] == 'year':
                item[splitted[0]] = int(splitted[1])
            elif splitted[0] == 'tempo' or splitted[0] == 'loudness':
                item[splitted[0]] = float(splitted[1])
            elif splitted[0] == 'explicit' or splitted[0] == 'instrumentalness':
                continue
            else:
                item[splitted[0]] = splitted[1]

data2 = []

with open(file="task_3_var_16_part_1.csv", mode="r", encoding='utf-8') as file:
    line_with_format = file.readline().strip()
    data_format = line_with_format.split(";")
    data_format_len = len(data_format)

    reader = csv.reader(file, delimiter=";", quotechar='"')
    for row in reader:
        if not row:
            continue

        if len(row) != data_format_len:
            raise Exception(f"row (`{row}`) mismatch format (`{data_format}`)")

        data2.append({column: data for column, data in zip(data_format, row)})


for elem in data2:
    elem.pop("energy")
    elem.pop("key")

    
drop_table(connection)

create_table(connection)

insert_data(connection, data1)
insert_data(connection, data2)

data = top_views(connection)
with open("t3_res_top_views.json", "w", encoding='utf-8') as file:
    json.dump(data, file, ensure_ascii=False)

print("Статистика по громкости: " + str(stat_loudness(connection)))

print("Статистика по жанрам: " + str(compute_freq_genre(connection)))

data = top_predicate_views(connection)
with open("t3_res_top_predicate_views.json", "w", encoding='utf-8') as file:
    json.dump(data, file, ensure_ascii=False)



