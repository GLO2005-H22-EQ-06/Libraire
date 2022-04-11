from datetime import datetime

import pandas as pd
import pymysql as sql

names = ["bookID", 'title', "authors", "average_rating", "isbn", "isbn13", "language_code", "num_pages",
         "ratings_count", "text_reviews_count", "publication_date", "publisher"]
df = pd.read_csv('./sql/books.csv', delimiter=',', names=names)
host = "root"
pwd = "root"
conn = sql.Connection(user="root", password=pwd,
                      host="localhost", database="projet_glo_2005")
conn.begin()
cursor = conn.cursor()
cursor.execute("SELECT  * FROM livres")
for x in cursor:
    print(x)
if not conn.open:
    print("hi")
    exit(0)
# command = f"""INSERT INTO LIVRES( ISBN, titre, auteur, langue, editeur, annee, nbrepages, description) values ({str(uuid.uuid4()), })"""
# cursor.execute()
n = 0
for index, row in df.iterrows():
    # print(row.values[0], row.values[10])
    com1 = "INSERT INTO LIVRES (ISBN, titre, langue, nbrepages, description ) " \
        "VALUES (%s, %s, %s, %s, %s)"
    #com2 = "INSERT INTO auteurs (nom) values (%s)"
    data1 = (
        str(row.values[5]), row.values[1], row.values[6], str(row.values[7]),
        "Rien à dire pour le moment")  # , datetime.strptime(row.values[10], '%m/%d/%Y'))
    # print(len(row.values[2]))
    # print(data)
    try:
        cursor.execute(com1, data1)
        conn.commit()
    except Exception as err:
        print(err)

# conn.commit()
conn.close()
