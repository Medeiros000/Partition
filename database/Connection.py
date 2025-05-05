import os
import psycopg2 as pg
import sqlite3 as sq
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
from abc import ABC, abstractmethod
from typing import Any, Optional


class ConnectionBase(ABC):
  @abstractmethod
  def get_connection(self) -> Any:
    """
    Abstract method to establish a connection to the database.
    """
    pass

  @abstractmethod
  def get_cursor(self, conn: Any) -> Any:
    """
    Abstract method to get a cursor from the connection.
    """
    pass

  def __enter__(self):
    """
    Context manager entry method to establish a connection.
    """
    self.conn = self.get_connection()
    self.cursor = self.get_cursor(self.conn)
    return self.conn, self.cursor

  def __exit__(self, exc_type, exc_val, exc_tb):
    """
    Context manager exit method to close the connection.
    """
    if hasattr(self, 'cursor') and self.cursor:
      self.cursor.close()
    if hasattr(self, 'conn') and self.conn:
      self.conn.close()


class PostgreSQLConfig:
  def __init__(self, db: Optional[str] = None, user: Optional[str] = None, host: Optional[str] = None, password: Optional[str] = None, port: Optional[str] = None):
    load_dotenv()
    self.db_database = db or os.getenv("PSQL_DATABASE")
    self.db_user = user or os.getenv("PSQL_USER")
    self.db_host = host or os.getenv("PSQL_HOST")
    self.db_password = password or os.getenv("PSQL_PASSWORD")
    self.db_port = port or os.getenv("PSQL_PORT")

  def get_url(self) -> str:
    return f"postgresql+psycopg2://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_database}"


class PostgreSQLConnection(ConnectionBase):
  def __init__(self, config: Optional[PostgreSQLConfig] = None):
    self.config = config or PostgreSQLConfig()
    self.name = "PostgreSQLConnection"

  def get_connection(self):
    try:
      conn = pg.connect(
          database=self.config.db_database,
          user=self.config.db_user,
          host=self.config.db_host,
          password=self.config.db_password,
          port=self.config.db_port
      )
      conn.autocommit = True
      return conn
    except Exception as e:
      raise ConnectionError(f"Error connecting to PostgreSQL: {e}") from e

  def get_cursor(self, conn):
    return conn.cursor()

  def get_url(self):
    return self.config.get_url()


class SQLiteConfig:
  def __init__(self, db_path: Optional[str] = None):
    self.db_path = db_path if db_path else ":memory:"

  def get_url(self) -> str:
    return f"sqlite:///{self.db_path}" if self.db_path != ":memory:" else "sqlite:///:memory:"


class SQLiteConnection(ConnectionBase):
  def __init__(self, config: Optional[SQLiteConfig] = None):
    self.config = config or SQLiteConfig()
    self.name = "SQLiteConnection"

  def get_connection(self):
    try:
      conn = sq.connect(self.config.db_path)
      conn.autocommit = True
      return conn
    except Exception as e:
      raise ConnectionError(f"Error connecting to SQLite: {e}") from e

  def get_cursor(self, conn):
    return conn.cursor()

  def get_url(self):
    return self.config.get_url()


class SqlAlchemyConnection(ConnectionBase):
  def __init__(self, db_url: Optional[str] = None):
    self.name = "SqlAlchemyConnection"
    self.db_url = db_url
    if not self.db_url:
      raise ValueError("db_url must be provided for SqlAlchemyConnection")

  def get_connection(self):
    try:
      engine = create_engine(self.db_url)
      conn = engine.connect()
      return conn
    except Exception as e:
      raise ConnectionError(f"Error connecting with SQLAlchemy: {e}") from e

  def get_cursor(self, conn):
    # SQLAlchemy connections do not use cursors in the same way
    return conn

  def get_engine(self):
    return create_engine(self.db_url)
