import mysql.connector

db_config = {
    'host': '127.0.0.1',
    'user': 'root',
    'password': 'Shaktiman@25',
    'database': 'project'
}

def connect_db():
    return mysql.connector.connect(**db_config)
