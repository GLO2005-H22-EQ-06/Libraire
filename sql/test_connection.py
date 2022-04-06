import pymysql


conn = pymysql.connect("localhost", "root", "EnvyUS123", "glo_2005_labs")

cursor = conn.cursor()
cursor.execute("SELECT  * FROM livres")
for x in cursor:
    print(x)
if not conn.open:
    exit(0)