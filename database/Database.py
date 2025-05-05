import re
from typing import List
from database.Connection import *


class Database:

  def __init__(self, conn: ConnectionBase = None):
    """
    Inicializa uma instância da classe Database com uma conexão injetada.
    """
    self.conn = conn if conn else PostgreSQLConnection()
    self.name = "Database"

  def execute_query(self, query: str, return_all: bool = False, return_one: bool = False) -> None | List:
    """
    Executa uma query SQL usando a conexão injetada.
    """
    try:
      with self.conn as (conn, cursor):
        cursor.execute(query)
        if return_one:
          result = cursor.fetchone()
          return result[0] if result else None
        if return_all:
          return cursor.fetchall()
    except Exception as e:
      print(f"Error executing query: {e}")
      return

  def show_insert_into(self, table_origin: str, table_destination: str) -> str:
    return f"INSERT INTO {table_destination} SELECT * FROM {table_origin};"

  def auxiliar_data(self, table: str, column: str) -> List:
    query = f"""SELECT ROW_NUMBER() OVER(ORDER BY {column}) AS id, {column}, COUNT(*) AS n_reg
                FROM {table} GROUP BY 2;"""
    return self.execute_query(query, return_all=True)

  def select_table(self, table: str, limit: int = None) -> List:
    query = f"SELECT * FROM {table} ORDER BY 1"
    query += f" LIMIT {limit}" if limit is not None else ""
    return self.execute_query(query, return_all=True)

  def show_create_table(self, table: str) -> str:
    schema_in, table_in = table.split('.')
    query = f"SELECT pg_get_tabledef('{schema_in}', '{table_in}', True)"
    result = self.execute_query(query, return_all=True)
    if result:
      return result[0][0].replace(' TABLESPACE pg_default;', '').replace('\n\n', '')
    return ""

  def create_index(self, table: str, column: str) -> None:
    query = f"CREATE INDEX {table}_{column}_idx ON {table} ({column});"
    self.execute_query(query)

  def create_partition_table(self, table: str, partition_list: List) -> None:
    query = self.show_create_table_partition(table, partition_list)
    self.execute_query(query)

  def show_create_table_partition(self, table: str, partition_list: List) -> str:
    cod_init, cod_end = partition_list
    values = f'{cod_init}_{cod_end}'
    if cod_init == cod_end:
      values = f'{cod_init}'
    return f"CREATE TABLE {table}_{values} PARTITION OF {table} FOR VALUES FROM ({cod_init}) TO ({cod_end + 1});"

  def show_create_table_by_range(self, table: str, column: str) -> str:
    return self.show_create_table(table) + f" PARTITION BY RANGE ({column});"

  def creat_table_by_range(self, table: str, column: str) -> None:
    query = self.show_create_table_by_range(table, column)
    self.execute_query(query)

  def drop_table(self, table: str) -> None:
    query = f"DROP TABLE IF EXISTS {table};"
    self.execute_query(query)
