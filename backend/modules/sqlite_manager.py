"""Defines and outliens teh SQL lite manager"""
#-------------------------------------------------
# Imports
#-------------------------------------------------
import threading
import sqlite3
import os
#from datetime import datetime
from typing import Any, List, Optional, Tuple
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor

#-------------------------------------------------
# Variables
#-------------------------------------------------

#-------------------------------------------------
# functions
#-------------------------------------------------

#-------------------------------------------------
# classes
#-------------------------------------------------
class SQLiteManager ():
    """Handles all SQL calls and actions."""
    _instance = None
    _lock = threading.Lock()
    _connection:sqlite3.Connection|None
    _executor:ThreadPoolExecutor|None
    _main_lock:threading.Lock
    
    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super(SQLiteManager, cls).__new__(cls)
                cls._instance._init()
            return cls._instance
    
    def _init (self):
        self._executor = ThreadPoolExecutor(max_workers=10)
        self._main_lock = threading.Lock()

    def connect(self, db_path: str, schema_file_path:str|None=None):
        """Connect to a SQLite database file with a unique ID."""
        with self._main_lock:
            Path(db_path).parent.mkdir(parents=True, exist_ok=True)
            conn = sqlite3.connect(db_path, check_same_thread=False)
            if schema_file_path is not None and os.path.isfile(schema_file_path):
                _schema = Path(schema_file_path).read_text(encoding='utf-8')
                conn.executescript(_schema)
                conn.commit()
            conn.row_factory = sqlite3.Row
            self._connection = conn

    def disconnect(self):
        """Close a specific connection."""
        with self._main_lock:
            if self._connection is not None:
                self._connection.close()
                self._connection = None
                
    def get_connection(self) -> Optional[sqlite3.Connection]:
        """Returns teh current connection if one is avalible"""
        return self._connection

    def execute(self, query: str, params: Tuple[Any, ...] = ()) -> List[sqlite3.Row]:
        """Run a query synchronously."""
        conn = self._connection
        if conn is None:
            raise ValueError("No connection found.")
        cursor = conn.cursor()
        cursor.execute(query, params)
        return cursor.fetchall()

    def execute_async(self, query: str, params: Tuple[Any, ...] = ()):
        """Run a query asynchronously."""
        if self._executor is not None:
            return self._executor.submit(self.execute, query, params)
        
    def fetchall(self):
        """Returns all found results"""
        conn = self._connection
        if conn is None:
            raise ValueError("No connection found.")
        cursor = conn.cursor()
        return cursor.fetchall()

    def fetchone(self):
        """returns first result found"""
        conn = self._connection
        if conn is None:
            raise ValueError("No connection found.")
        cursor = conn.cursor()
        return cursor.fetchone()

        
#-------------------------------------------------
# Initilization
#-------------------------------------------------          

SQLite_Man = SQLiteManager()
