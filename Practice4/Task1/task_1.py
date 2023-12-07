import os
import sqlite3
import json

dbPath = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "db/DB1")

def connect(path):
    connection = sqlite3.connect(path)
    connection.row_factory = sqlite3.Row
    return connection


def drop_table(connection):
    connection.execute('''DROP TABLE IF EXISTS table1; ''')
    
def create_table(connection):
    connection.execute('''
CREATE TABLE table1 (
    id         INTEGER    PRIMARY KEY AUTOINCREMENT
                          NOT NULL
                          UNIQUE,
    name       TEXT (256) NOT NULL,
    city    TEXT (256) NOT NULL,
    begin       TEXT (256) NOT NULL,
    system    TEXT (256)    NOT NULL,
    tours_count     INTEGER    NOT NULL,
    min_rating       INTEGER    NOT NULL,
    time_on_game INTEGER    NOT NULL
);
''')
    
def insert_data(connection, data):
    cursor = connection.cursor()
    cursor.executemany(
        """
        INSERT INTO table1 (name, city, begin, system, tours_count, min_rating, time_on_game) 
        VALUES(:name, :city, :begin, :system, :tours_count, :min_rating, :time_on_game)
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
        ORDER BY min_rating DESC LIMIT ?
        ''', [top]
    )   
    items = []
    for row in res.fetchall():
        items.append(dict(row))
    cursor.close() 
    return items

def stat_time_on_game(connection):
    cursor = connection.cursor()
    res = cursor.execute(
        '''
        SELECT 
            SUM(time_on_game) as sum,
            AVG(time_on_game) as avg,
            MIN(time_on_game) as min, 
            MAX(time_on_game) as max
        FROM table1
        '''
    )
    res = dict(res.fetchone())
    cursor.close()
    return res

def compute_freq_system(connection):
    cursor = connection.cursor()
    res = cursor.execute(
        '''
        SELECT 
            CAST(COUNT(*) as REAL) / (SELECT COUNT(*) FROM table1) as count,
            system
        FROM table1
        GROUP BY system
        '''
    )

    stat_freq = []
    for row in res.fetchall():
        stat_freq.append(dict(row))

    cursor.close()
    return stat_freq

def top_predicate_views(connection, rating = 2300, top=11):
    cursor = connection.cursor()
    res = cursor.execute(
        '''
        SELECT * 
        FROM table1 
        WHERE min_rating >= ?
        ORDER BY system DESC LIMIT ?
        ''', [rating, top]
    )
    
    items = []
    for row in res.fetchall():
        items.append(dict(row))
    cursor.close()
    
    return items


connection = connect(dbPath)

data = []
with open("task_1_var_16_item.json", 'r', encoding='utf-8') as file:
    data_js = json.load(file)
    for elem in data_js:
        data.append(elem)
        
drop_table(connection)

create_table(connection)

insert_data(connection, data)

data = top_views(connection)
with open("t1_res_top_views.json", "w",encoding='utf-8') as file:
    json.dump(data, file, ensure_ascii=False)

print("Cтатистика по времени игры: " + str(stat_time_on_game(connection)))


print("Подсчет частоты встречаемости по типам турнирной сетки: " + str(compute_freq_system(connection)))

data = top_predicate_views(connection)
with open("t1_res_top_predicate_views.json", "w", encoding='utf-8') as file:
    json.dump(data, file, ensure_ascii=False)



