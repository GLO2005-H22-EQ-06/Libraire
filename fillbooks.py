import uuid
from datetime import datetime

import pandas as pd
import pymysql as sql

names = ["bookID", 'title', "authors", "average_rating", "isbn", "isbn13", "language_code", "num_pages",
         "ratings_count", "text_reviews_count", "publication_date", "publisher"]
df = pd.read_csv("books.csv", delimiter=',', names=names)
host = "root"
pwd = "root"
conn = sql.Connection(user=host, password=pwd, host="localhost", database="glo_2005_labs")
conn.begin()
cursor = conn.cursor()
cursor.execute("SELECT  * FROM livres")
for x in cursor:
    print(x)
if not conn.open:
    exit(0)
# command = f"""INSERT INTO LIVRES( ISBN, titre, auteur, langue, editeur, annee, nbrepages, description) values ({str(uuid.uuid4()), })"""
# cursor.execute()
n = 0
for index, row in df.iterrows():
    # print(row.values[0], row.values[10])
    command = "INSERT INTO LIVRES (id_produit, ISBN, titre, auteur, langue, editeur, nbrepages, description, annee ) " \
              "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
    data = (
    str(uuid.uuid4()), row.values[5], row.values[1], row.values[2], row.values[6], row.values[11], str(row.values[7]),
    "Rien à dire pour le moment", datetime.strptime(row.values[10], '%m/%d/%Y'))
    # print(len(row.values[2]))
    # print(data)
    try:
        cursor.execute(command, data)
        conn.commit()
    except:
        conn.rollback()
        n += 1
# conn.commit()
conn.close()
