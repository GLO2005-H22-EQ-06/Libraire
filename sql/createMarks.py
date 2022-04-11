import pymysql as sql

marks = ['Asus', 'Acer', "Dell", "HP", "Lenovo", "MSI"]
modeles = {
    'Asus': ['ROG', 'TUF', 'Vivobook', 'Zenbook'],
    'Acer': ["Aspire", "Nitro", 'Swift'],
    "Dell": ["Inspiron"],
    "HP": ["Envy", "Omen", "Pavilion"],
    "Lenovo": ["Ideapad", "Legion", "Yoga"],
    "MSI": ["Alpha", "Gfthin"]
}
"""screen = [13, 14, 15, 17]
ram = [2, 4, 6, 8, 16, 32, 64]
processeur = []
autonomie = [3, 4, 5, 6, 8, 10, 12]
stockage = []"""
# names = ["id", "price", "speed", "hd", "ram", "screen", "cd", "multi", "premium", "ads", "trend"]
# df = pd.read_csv('./sql/books.csv', delimiter=',', names=names)
host = "root"
pwd = "root"
conn = sql.Connection(user="root", password=pwd,
                      host="localhost", database="glo_2005_labs")
conn.begin()
cursor = conn.cursor()
command = f"INSERT INTO marques VALUES (%s, %s)"
for mark in marks:
    for model in modeles[mark]:
        data = (mark, model)
        print(data)
        cursor.execute(command, data)
        conn.commit()


conn.close()

# cursor.execute("INSERT INTO marques VALUES ()")
