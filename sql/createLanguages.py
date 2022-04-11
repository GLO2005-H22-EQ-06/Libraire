import pandas as pd
import pymysql as sql


df = pd.read_csv('../glo_2005_labs_livres.csv', delimiter=',')
dictio = {}
i = 0
host = "root"
pwd = "13Loulou#"
conn = sql.Connection(user="root", password=pwd,
                      host="localhost", database="glo_2005_labs")
conn.begin()
cursor = conn.cursor()
command = "INSERT INTO langues (code_lang) VALUES (%s)"
for index, row in df.items():
    cursor.execute(command, (index))
    conn.commit()
conn.close()