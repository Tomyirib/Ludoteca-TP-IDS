import mysql.connector
import json
from backend.steam_service import get_all_games_data

conn = mysql.connector.connect (
    host="localhost",
    user="root",
    password="root"
)
#cursor = conn.cursor()

#with open("init_db.sql", "r") as file:
#    init_db = file.read()

#for linea in cursor.execute(init_db, multi=True):
#    pass

data = get_all_games_data()

def generate_insert_query():
    data = get_all_games_data()[0]
    generar_insert_sql("juegos", data)
    

def generar_insert_sql(name, data):
    
    insert_statements = []
    for game in data:
        print(type(data))              # ¿Es lista?
        print(type(data[0]))           # ¿Es dict o str?
        print(data[0])  
        columns = []
        values = []

        for key, value in game.items():
            columns.append(key)

            # Formateamos el valor adecuadamente
            if isinstance(value, str):
                values.append(f"'{value.replace('\'', '\'\'')}'")  # Escapar comillas simples
            elif isinstance(value, (int, float)):
                values.append(str(value))
            elif isinstance(value, list) or isinstance(value, dict):
                json_str = json.dumps(value).replace("'", "''")
                values.append(f"'{json_str}'")
            elif value is None:
                values.append("NULL")
            else:
                values.append(f"'{str(value)}'")

        cols_str = ", ".join(columns)
        vals_str = ", ".join(values)

        insert_sql = f"INSERT INTO {name} ({cols_str}) VALUES ({vals_str});"
        insert_statements.append(insert_sql)

    # Mostrar todos los INSERTs
    for stmt in insert_statements:
        print(stmt)
#cursor.close()
#conn.close()