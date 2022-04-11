import pandas as pd
import pymysql as sql

df = pd.read_csv('../auteurs.csv', delimiter=',')
dictio = {}
i = 0
host = "root"
pwd = "13Loulou#"
conn = sql.Connection(user="root", password=pwd,
                      host="localhost", database="projet_glo_2005")
conn.begin()
cursor = conn.cursor()
command = "INSERT INTO auteurs (nom) VALUES (%s)"
# print(df)
for index, row in df.items():
    # print(index)
    cursor.execute(command, (index[0:249]))
    conn.commit()
conn.close()
