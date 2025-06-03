import mysql.connector
from backend.steam_service import get_all_games_data

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

data = get_all_games_data()

def generate_insert_query(data):
    data = get_all_games_data()
    

def generar_insert_sql(nombre_tabla, datos):
    columnas = list(datos.keys())
    valores = []

    for valor in datos.values():
        if valor is None:
            valores.append("NULL")
        elif isinstance(valor, str):
            replaces = valor.replace("'", "''")  # Escapa comillas simples para SQL
            valores.append(f"'{replaces}'")
        elif isinstance(valor, bool):
            valores.append("TRUE" if valor else "FALSE")
        else:
            valores.append(str(valor))

    columnas_sql = ", ".join(columnas)
    valores_sql = ", ".join(valores)

    return f"INSERT INTO {nombre_tabla} ({columnas_sql}) VALUES ({valores_sql});"



cursor.close()
conn.close()