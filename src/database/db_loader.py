import sqlite3
from pathlib import Path
from typing import Optional, List, Dict, Any


class DatabaseLoader:
    
    def __init__(self, db_path: str):
        self.db_path = Path(db_path)
        if not self.db_path.exists():
            raise FileNotFoundError(f"Database file not found: {db_path}")
        self.connection = None
    
    def connect(self) -> None:
        self.connection = sqlite3.connect(str(self.db_path))
        self.connection.row_factory = sqlite3.Row
    
    def disconnect(self) -> None:
        if self.connection:
            self.connection.close()
            self.connection = None
    
    def execute_query(self, query: str, params: Optional[tuple] = None) -> List[Dict[str, Any]]:
        if not self.connection:
            self.connect()
            
        cursor = self.connection.cursor()
        
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
            
        results = [dict(row) for row in cursor.fetchall()]
        cursor.close()
        
        return results
    
    def get_table_names(self) -> List[str]:
        query = "SELECT name FROM sqlite_master WHERE type='table';"
        results = self.execute_query(query)
        return [row['name'] for row in results]
    
    def get_table_schema(self, table_name: str) -> List[Dict[str, Any]]:
        query = f"PRAGMA table_info({table_name});"
        return self.execute_query(query)
    
    def get_foreign_keys(self, table_name: str) -> List[Dict[str, Any]]:
        query = f"PRAGMA foreign_key_list({table_name});"
        return self.execute_query(query)
    
    def get_tables(self) -> List[Dict[str, Any]]:
        query = "SELECT name FROM sqlite_master WHERE type='table';"
        return self.execute_query(query)
    
    def __enter__(self):
        self.connect()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.disconnect()
