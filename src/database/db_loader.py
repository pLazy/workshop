import sqlite3
from pathlib import Path
from typing import Optional, List, Dict, Any


class DatabaseLoader:
    """
    A class to load and interact with SQLite databases.
    """
    
    def __init__(self, db_path: str):
        """
        Initialize the DatabaseLoader with the path to the SQLite database.
        
        Args:
            db_path: Path to the SQLite database file
        """
        self.db_path = Path(db_path)
        print(f"Database path: {self.db_path}")
        if not self.db_path.exists():
            raise FileNotFoundError(f"Database file not found: {db_path}")
        
        self.connection = None
    
    def connect(self) -> None:
        """
        Establish a connection to the SQLite database.
        """
        self.connection = sqlite3.connect(str(self.db_path))
        self.connection.row_factory = sqlite3.Row
    
    def disconnect(self) -> None:
        """
        Close the connection to the SQLite database.
        """
        if self.connection:
            self.connection.close()
            self.connection = None
    
    def execute_query(self, query: str, params: Optional[tuple] = None) -> List[Dict[str, Any]]:
        """
        Execute an SQL query and return the results.
        
        Args:
            query: SQL query string
            params: Optional parameters for the query
            
        Returns:
            List of dictionaries representing the query results
        """
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
        """
        Get a list of all table names in the database.
        
        Returns:
            List of table names
        """
        query = "SELECT name FROM sqlite_master WHERE type='table';"
        results = self.execute_query(query)
        return [row['name'] for row in results]
    
    def get_table_schema(self, table_name: str) -> List[Dict[str, Any]]:
        """
        Get the schema for a specific table.
        
        Args:
            table_name: Name of the table
            
        Returns:
            List of dictionaries containing column information
        """
        query = f"PRAGMA table_info({table_name});"
        return self.execute_query(query)
    
    def __enter__(self):
        """
        Context manager entry point.
        """
        self.connect()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Context manager exit point.
        """
        self.disconnect()
