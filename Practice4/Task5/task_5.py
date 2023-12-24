import os
import sqlite3
import json
import csv
import msgpack
import pandas as pd

dbPath = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "db/DB4")

def connect(path):
    connection = sqlite3.connect(path)
    connection.row_factory = sqlite3.Row
    return connection


def data_from_json():
    with open("data.json", 'r', encoding='utf-8') as file:
        items = json.load(file)
    return items

def csv_data():
    df = pd.read_csv('cwurData.csv')
    print(df)
    conn = sqlite3.connect(dbPath)
    conn.row_factory = sqlite3.Row
    df.to_sql('table1', conn)
    conn.close()

    
def data_from_csv():
    with open("cwurData.csv", encoding='utf-8') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=';')
        titles = spamreader.__next__()
        items = []
        for row in spamreader:
            item = {}
            for i in range(len(row)):
                try:
                    if "world_rank" == titles[i]:
                        item["world_rank"] = int(row[i])
                    elif "national_rank" == titles[i]:
                        item["national_rank"] = int(row[i])
                    elif "quality_of_education" == titles[i]:
                        item["quality_of_education"] = int(row[i])
                    elif "quality_of_faculity" == titles[i]:
                        item["quality_of_faculity"] = int(row[i])
                    elif "alumni_employment" == titles[i]:
                        item["alumni_employment"] = int(row[i])
                    elif "publications" == titles[i]:
                        item["publications"] = int(row[i])
                    elif "influence" == titles[i]:
                        item["influence"] = int(row[i])
                    elif "citations" == titles[i]:
                        item["citations"] = int(row[i])
                    elif "patents" == titles[i]:
                        item["patents"] = int(row[i])
                    elif "score" == titles[i]:
                        item["score"] = float(row[i])
                    elif "year" == titles[i]:
                        item["year"] = int(row[i])
                    else:
                        item[titles[i]] = row[i].strip('"')
                except:
                    print()
            items.append(item)
    return items


    
def drop_table(connection):
    connection.execute('''DROP TABLE IF EXISTS table1; ''')
    
def create_table1(connection):
    connection.execute('''
CREATE TABLE table1 (
    id          INTEGER    PRIMARY KEY AUTOINCREMENT
                           UNIQUE
                           NOT NULL,
    world_rank  INTEGER    NOT NULL,
    institution     TEXT(256)  NOT NULL,
    country     TEXT(256)  NOT NULL,
    national_rank  INTEGER    NOT NULL,
    quality_of_education  INTEGER    NOT NULL,
    alumni_employment  INTEGER    NOT NULL,
    quality_of_faculty  INTEGER    NOT NULL,
    publications  INTEGER    NOT NULL,
    influence  INTEGER    NOT NULL,
    citations  INTEGER    NOT NULL,
    broad_impact INTEGER NOT NULL,
    patents  INTEGER    NOT NULL,
    score  FLOAT    NOT NULL,
    year    INTEGER NOT NULL
)

''')

def create_table2(connection):
    connection.execute('''
CREATE TABLE table1 (
    id          INTEGER    PRIMARY KEY AUTOINCREMENT
                           UNIQUE
                           NOT NULL
)

''')

def create_table3(connection):
    connection.execute('''
CREATE TABLE table1 (
    id          INTEGER    PRIMARY KEY AUTOINCREMENT
                           UNIQUE
                           NOT NULL
)

''')
    
def insert_data(connection, data):
    cursor = connection.cursor()
    cursor.executemany(
        """
        INSERT INTO table1 (world_rank, institution, country, national_rank, quality_of_education, alumni_employment, quality_of_faculty, publications, influence, citations, patents, score, year) 
        VALUES(:world_rank, :institution, :country, :national_rank, :quality_of_education, :alumni_employment, :quality_of_faculty, :publications, :influence, :citations, :patents, :score, :year)
        """, data
    )
    connection.commit()
    cursor.close()

def top_views(connection, top=10):
    cursor = connection.cursor()
    res = cursor.execute(
        '''
        SELECT * 
        FROM table1 
        ORDER BY national_rank DESC LIMIT ?
        ''', [top]
    )   
    items = []
    for row in res.fetchall():
        items.append(dict(row))
    cursor.close()  
    return items

def stat_score(connection):
    cursor = connection.cursor()
    res = cursor.execute(
        '''
        SELECT 
            country,
            CAST(COUNT(*) as REAL) as count,
            SUM(score) as sum,
            AVG(score) as avg,
            MIN(score) as min, 
            MAX(score) as max
        FROM table1
        GROUP BY country
        '''
    )
    stat_freq = []
    for row in res.fetchall():
        stat_freq.append(dict(row))

    cursor.close()
    return stat_freq


def stat_citations(connection):
    cursor = connection.cursor()
    res = cursor.execute(
        '''
        SELECT 
            country,
            CAST(COUNT(*) as REAL) as count,
            SUM(citations) as sum,
            AVG(citations) as avg,
            MIN(citations) as min, 
            MAX(citations) as max
        FROM table1
        GROUP BY country
        '''
    )
    stat_freq = []
    for row in res.fetchall():
        stat_freq.append(dict(row))
    cursor.close()
    return stat_freq


def top_predicate_views(connection, country="USA", top=15):
    cursor = connection.cursor()
    res = cursor.execute(
        '''
        SELECT * 
        FROM table1 
        WHERE country = ?
        ORDER BY score DESC LIMIT ?
        ''', [country, top]
    )  
    items = []
    for row in res.fetchall():
        items.append(dict(row))
    cursor.close()   
    return items

def remove(connection, limit):
    cursor = connection.cursor()
    cursor.execute(
        '''
        DELETE FROM table1 
        WHERE quality_of_education < ?
        ''', [limit]
    )
    connection.commit()
    cursor.close()

def year_inc(connection, amount):
    cursor = connection.cursor()
    cursor.execute(
        '''
        UPDATE table1 
        SET year = year + ?
        ''', [amount]
    )    
    connection.commit()
    cursor.close()

connection = connect(dbPath)

data2 = data_from_json()

    
drop_table(connection)


csv_data()
insert_data(connection, data2)

remove(connection, 30)
year_inc(connection, 11)

data = top_views(connection)
with open("t5_res_top_views.json", "w", encoding='utf-8') as file:
    json.dump(data, file, ensure_ascii=False)

data = top_predicate_views(connection)
with open("t5_res_top_predicate_views.json", "w", encoding='utf-8') as file:
    json.dump(data, file, ensure_ascii=False)

data = stat_score(connection)
with open("t5_res_stat_score.json", "w", encoding='utf-8') as file:
    json.dump(data, file, ensure_ascii=False)

data = stat_citations(connection)
with open("t5_res_stat_citations.json", "w", encoding='utf-8') as file:
    json.dump(data, file, ensure_ascii=False)




