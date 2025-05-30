import mysql.connector

conn = mysql.connector.connect (
    host="localhost",
    user="root",
    password="root"
)
cursor = conn.cursor()

with open("init_db.sql", "r") as file:
    init_db = file.read()

for linea in cursor.execute(init_db, multi=True):
    pass

print("Base de datos inicializada")

cursor.close()
conn.close()