import mysql.connector.pooling
from dotenv import load_dotenv
import os
from helpers.logs import Log, ERROR

load_dotenv()

mysql_user = os.getenv('MYSQL_USER')
mysql_password = os.getenv('MYSQL_USER_PASSWORD')
mysql_database = os.getenv('MYSQL_DATABASE')

log = Log()

try:
    pool = mysql.connector.pooling.MySQLConnectionPool(
        pool_name="pool",
        pool_size=5,
        host="mysql",
        user=mysql_user,
        password=mysql_password,
        database=mysql_database
    )
except mysql.connector.Error as e:
    log.log(f"Failed to create pool to MySQL database: {e}", ERROR)
    raise e


def init_table(name: str, structure: str):
    connection = pool.get_connection()
    cursor = connection.cursor()
    query = f"CREATE TABLE IF NOT EXISTS {name} ({structure})"
    cursor.execute(query)
    connection.commit()
    cursor.close()
    connection.close()


def get_records(table: str, filter: str = None) -> list:
    connection = pool.get_connection()
    cursor = connection.cursor()
    if filter:
        query = f"SELECT * FROM {table} WHERE {filter}"
    else:
        query = f"SELECT * FROM {table}"
    cursor.execute(query)
    records = cursor.fetchall()
    cursor.close()
    connection.close()
    return records


def insert_record(table: str, columns: tuple, data: tuple) -> int:
    connection = pool.get_connection()
    cursor = connection.cursor()
    columns_str = ', '.join(columns)
    placeholders = ', '.join(['%s'] * len(data))
    query = f"INSERT INTO {table} ({columns_str}) VALUES ({placeholders})"
    cursor.execute(query, data)
    connection.commit()
    num_rows = cursor.rowcount
    cursor.close()
    connection.close()
    return num_rows


def update_record(table: str, data: tuple, filter: str) -> int:
    connection = pool.get_connection()
    cursor = connection.cursor()
    query = f"UPDATE {table}\
              SET {', '.join([f'{key}=%s' for key in data.keys()])}\
              WHERE {filter}"
    cursor.execute(query, tuple(data.values()))
    connection.commit()
    num_rows = cursor.rowcount
    cursor.close()
    connection.close()
    return num_rows


def delete_record(table: str, filter: str) -> int:
    connection = pool.get_connection()
    cursor = connection.cursor()
    query = f"DELETE FROM {table} WHERE {filter}"
    cursor.execute(query)
    connection.commit()
    row_count = cursor.rowcount
    cursor.close()
    connection.close()
    return row_count
