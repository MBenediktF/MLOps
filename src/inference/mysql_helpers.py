import mysql.connector
from dotenv import load_dotenv
import os
from log_message import log_message, INFO, ERROR

load_dotenv()

mysql_user = os.getenv('MYSQL_USER')
mysql_password = os.getenv('MYSQL_USER_PASSWORD')
mysql_database = os.getenv('MYSQL_DATABASE')

try:
    mysql_client = mysql.connector.connect(
        host="mysql",
        user=mysql_user,
        password=mysql_password,
        database=mysql_database
    )
except mysql.connector.Error as e:
    log_message(f"Failed to connect to MySQL database: {e}", ERROR)
    raise e

if mysql_client.is_connected():
    log_message("Connected to MySQL database", INFO)

mysql_cursor = mysql_client.cursor()


def init_table(name: str, structure: str):
    query = f"CREATE TABLE IF NOT EXISTS {name} ({structure})"
    mysql_cursor.execute(query)
    mysql_client.commit()


def get_records(table: str, filter: str = None) -> list:
    if filter:
        query = f"SELECT * FROM {table} WHERE {filter}"
    else:
        query = f"SELECT * FROM {table}"
    mysql_cursor.execute(query)
    return mysql_cursor.fetchall()


def insert_record(table: str, columns: tuple, data: tuple) -> int:
    columns_str = ', '.join(columns)
    placeholders = ', '.join(['%s'] * len(data))
    query = f"INSERT INTO {table} ({columns_str}) VALUES ({placeholders})"
    mysql_cursor.execute(query, data)
    mysql_client.commit()
    return mysql_cursor.rowcount


def update_record(table: str, data: tuple, filter: str) -> int:
    query = f"UPDATE {table}\
              SET {', '.join([f'{key}=%s' for key in data.keys()])}\
              WHERE {filter}"
    mysql_cursor.execute(query, tuple(data.values()))
    mysql_client.commit()
    return mysql_cursor.rowcount


def delete_record(table: str, filter: str) -> int:
    query = f"DELETE FROM {table} WHERE {filter}"
    mysql_cursor.execute(query)
    mysql_client.commit()
    return mysql_cursor.rowcount
