import pymysql as sql

host = "root"
pwd = "13Loulou#"
conn = sql.Connection(user=host, password=pwd, host="localhost", database="glo_2005_labs")
conn.begin()
cursor = conn.cursor()
cursor.execute("SELECT  * FROM livres")
for x in cursor:
    print(x)
if not conn.open:
    exit(0)