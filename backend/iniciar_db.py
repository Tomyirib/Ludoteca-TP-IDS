import os
import mysql.connector

conn = mysql.connector.connect (
    host="localhost",
    user="root",
    password="root"
)
cursor = conn.cursor()

def iniciar_db():
    print("Iniciando base de datos...")
    

sql_path = os.path.join(os.path.dirname(__file__), "init_db.sql")
with open(sql_path, "r") as file:
    init_db = file.read()

for linea in cursor.execute(init_db, multi=True):
    pass

print("Base de datos inicializada")

cursor.close()
conn.close()