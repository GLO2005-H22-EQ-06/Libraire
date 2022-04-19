import uuid

import lorem
import random
from datetime import datetime
import pandas as pd
import pymysql as sql
import bcrypt

host = "root"
pwd = "13Loulou#"
salt = b'$2b$12$R2Yw1fjNG8loy69c8PrWWO'
conn = sql.Connection(user="root", password=pwd,
                      host="localhost", database="projet_glo_2005")
conn.begin()
cursor = conn.cursor()


def createId(prenom: str, nom: str):
    return prenom[0:2] + nom[0:2]


prenoms = ("Noah", "Jackson", "Liam", "Lucas", "Olivier", "Leo", "Benjamin", "Theo", "Jack", "Aiden")
noms = ("Allen", "Bell", "Brown", "Chan", "Jones", "Ross", "Scott", "Wong", "Young", "Moore")
phones = ("9842918448",
          "8125873787",
          "8263893759",
          "8508945183",
          "2837720228",
          "7897272804",
          "2372847381",
          "2017464475",
          "6758280126",
          "5734043732")
emails = ("dcemgrg045@gaduguda.xyz", "wmqnvoc461@gaduguda.xyz", "jusjeud668@couldmail.com", "qvrrymr310@gaduguda.xyz",
          "tpprtzm173@uptoupmail.com", "tprtzm173@uptoupmail.com", "zyxdinx471@couldmail.com",
          "sbyniip439@uptoupmail.com",
          "ddyehfj848@uptoupmail.com", "fwzbkpu087@uptoupmail.com")
for i in range(10):
    id_client = uuid.uuid4()
    iden = createId(prenoms[i], noms[i]).lower()
    cursor.execute("INSERT INTO clients VALUES (%s, %s, %s, %s, %s, %s)", (id_client, noms[i], prenoms[i], emails[i], lorem.sentence(), phones[i]))
    cursor.execute("INSERT INTO projet_glo_2005.compte values(%s, %s)", (iden, bcrypt.hashpw(lorem.sentence().encode("utf-8"), salt) ))
    conn.commit()
    cursor.execute("INSERT INTO projet_glo_2005.associer VALUES(%s, %s)", (iden, id_client))
    conn.commit()
