import os
import sqlite3
import json

dbPath = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "db/DB1")

def connect(path):
    connection = sqlite3.connect(path)
    connection.row_factory = sqlite3.Row
    return connection


def drop_table(connection):
    connection.execute('''DROP TABLE IF EXISTS table2; ''')
    
def create_table(connection):
    connection.execute('''
CREATE TABLE table2 (
    id            INTEGER    UNIQUE
                             PRIMARY KEY AUTOINCREMENT
                             NOT NULL,
    id_table1     INTEGER    REFERENCES table1 (id) 
                             NOT NULL,
    place   INTEGER    NOT NULL,
    prise      INTEGER    NOT NULL
);

''')
    
def insert_data(connection, data):
    cursor = connection.cursor()
    cursor.executemany(
        """
        INSERT INTO table2 (id_table1, place, prise) 
        VALUES(
            (SELECT id FROM table1 WHERE name = :name),
            :place, :prise)
        """, data
    )
    connection.commit()
    cursor.close()

def q1(connection, city="Хихон"):
    cursor = connection.cursor()
    res = cursor.execute(
    '''
        SELECT table2.* 
        FROM table2, table1
        WHERE table2.id_table1 = table1.id AND table1.city = ?              
    ''', [city])
    
    items = []
    for row in res.fetchall():
        items.append(dict(row))
    cursor.close()
    return items   

def stat_prise(connection):
    cursor = connection.cursor()
    res = cursor.execute(
        '''
        SELECT 
            SUM(table2.prise) as sum,
            AVG(table2.prise) as avg,
            MIN(table2.prise) as min, 
            MAX(table2.prise) as max
        FROM table2, table1
        WHERE table2.id_table1 = table1.id
        '''
    )
    res = dict(res.fetchone())
    cursor.close()
    return res

def q3(connection, min_rating=2300, max_rating=2500):
    cursor = connection.cursor()
    res = cursor.execute(
        '''
        SELECT table2.*
        FROM table2, table1
        WHERE table2.id_table1 = table1.id AND table1.min_rating > ? AND table1.min_rating < ? 
        ''', [min_rating, max_rating]
    )

    stat_freq = []
    for row in res.fetchall():
        stat_freq.append(dict(row))

    cursor.close()
    return stat_freq

connection = connect(dbPath)

data = []
with open("task_2_var_16_subitem.json", 'r', encoding='utf-8') as file:
    data_js = json.load(file)
    for elem in data_js:
        data.append(elem)
        
drop_table(connection)

create_table(connection)

insert_data(connection, data)

data = q1(connection)
with open("t1_res_1.json", "w", encoding='utf-8') as file:
    json.dump(data, file, ensure_ascii=False)

print("Cтатистика по призовым: " + str(stat_prise(connection)))

data = q3(connection)
with open("t1_res_3.json", "w", encoding='utf-8') as file:
    json.dump(data, file, ensure_ascii=False)



