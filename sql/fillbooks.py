import random
from datetime import datetime

import lorem
import pandas as pd
import pymysql as sql

names = ["bookID", 'title', "authors", "average_rating", "isbn", "isbn13", "language_code", "num_pages",
         "ratings_count", "text_reviews_count", "publication_date", "publisher"]
df = pd.read_csv('../csv/books.csv', delimiter=',', names=names)
host = "root"
pwd = "EnvyUS123"

conn = sql.Connection(user="root", password=pwd,
                      host="localhost", database="projet_glo_2005")
conn.begin()
cursor = conn.cursor()

n = 0
for index, row in df.iterrows():
    # print(row.values[0], row.values[10])
    com1 = "INSERT INTO LIVRES (ISBN, titre, langue, auteur, editeur, nbrepages, description, annee, prix) " \
           "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
    com2 = "INSERT INTO STOCK values (%s, %s)"
    data2 = (row.values[4], random.randint(1, 250))
    data1 = (str(row.values[4]), row.values[1][0:249], row.values[6], row.values[2][0:249],
             row.values[11], str(row.values[7]), lorem.paragraph(),
             datetime.strptime(row.values[10], '%m/%d/%Y'), round(random.uniform(30, 250), 2))
    try:
        cursor.execute(com1, data1)
        cursor.execute(com2, data2)
        conn.commit()
    except Exception as err:
        print(err)

conn.close()
