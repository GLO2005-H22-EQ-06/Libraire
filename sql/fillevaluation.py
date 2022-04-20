import random
from datetime import datetime

import lorem
import pandas as pd
import pymysql as sql

host = "root"
pwd = "13Loulou#"
conn = sql.Connection(user="root", password=pwd,
                      host="localhost", database="projet_glo_2005")
conn.begin()
cursor = conn.cursor()

liste = []

cursor.execute("select id_client from clients")
clients = cursor.fetchall()

cursor.execute('select isbn from livres limit 150')
livres = cursor.fetchall()
i = 0
while i < 800:
    client = random.choice(clients)
    isbn = random.choice(livres)
    if (client, isbn) not in liste:
        liste.append((client,isbn))
        i += 1
        cursor.execute('insert into evaluer (id_client, isbn, note, commentaire, date) values(%s, %s, %s, %s, now())',
                       (client, isbn, random.randint(0, 5), lorem.sentence()))
        conn.commit()
