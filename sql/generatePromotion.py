import pymysql as sql
import random
from datetime import datetime, timedelta


host = "root"
pwd = "EnvyUS123"
conn = sql.Connection(user="root", password=pwd,
                      host="localhost", database="projet_glo_2005")
conn.begin()
cursor = conn.cursor()


def generate_promotion():
    for i in range(10):
        comm = "insert into promotions values (%s, %s, %s, %s)"
        data = (0, round(random.uniform(15, 90), 2), datetime.now(),
                datetime.now() + timedelta(days=random.randint(3, 20)))

        try:
            cursor.execute(comm, data)
            conn.commit()
        except Exception as err:
            print(err)


def appliquer_promotion():
    cursor.execute('select isbn from livres limit 1000')
    books = cursor.fetchall()

    cursor.execute('select id_promotion from promotions')
    promotions = cursor.fetchall()

    for isbn in books:
        id_promo = random.choice(promotions)
        cursor.execute('insert into appliquer values (%s, %s, %s)',
                       (id_promo, isbn, 0))
        conn.commit()


if __name__ == "__main__":
    generate_promotion()
    appliquer_promotion()