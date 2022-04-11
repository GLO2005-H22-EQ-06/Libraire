import pandas as pd
import pymysql as sql

df = pd.read_csv('./sql/editeurs.csv', delimiter=',')
dictio = {}
i = 0
host = "root"
pwd = "root"
conn = sql.Connection(user="root", password=pwd,
                      host="localhost", database="projet_glo_2005")
conn.begin()
cursor = conn.cursor()
command = "INSERT INTO editeurs (nom) VALUES (%s)"
for index, row in df.items():
    cursor.execute(command, (index))
    conn.commit()
conn.close()
