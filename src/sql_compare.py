import sqlite3
import pandas as pd
import hashlib
from typing import Tuple, Dict, Any
import json

class SQLQueryComparator:
    def __init__(self, db_connection):
        self.conn = db_connection
        
    def get_query_metadata(self, query: str) -> Dict[str, Any]:
        """Get metadata about a query's result structure"""
        try:
            # Create a temp table with 0 rows to get structure
            temp_name = f"temp_meta_{hash(query) % 100000}"
            self.conn.execute(f"CREATE TEMP TABLE {temp_name} AS {query} LIMIT 0")
            
            # Get column info
            cursor = self.conn.execute(f"PRAGMA table_info({temp_name})")
            columns = [(row[1], row[2]) for row in cursor.fetchall()]  # (name, type)
            
            # Clean up
            self.conn.execute(f"DROP TABLE {temp_name}")
            
            return {
                'columns': columns,
                'column_count': len(columns),
                'column_names': [col[0] for col in columns],
                'column_types': [col[1] for col in columns]
            }
        except Exception as e:
            raise Exception(f"Error analyzing query metadata: {e}")
    
    def normalize_query_results(self, query: str, target_columns: list = None) -> str:
        """Normalize query to return consistent columns for comparison"""
        if target_columns is None:
            # Return as-is for metadata analysis
            return query
            
        # Build SELECT clause with target columns
        select_parts = []
        query_meta = self.get_query_metadata(query)
        available_columns = query_meta['column_names']
        
        for col in target_columns:
            if col in available_columns:
                select_parts.append(col)
            else:
                select_parts.append(f"NULL as {col}")
        
        # Wrap original query and select normalized columns
        normalized = f"""
        SELECT {', '.join(select_parts)}
        FROM ({query}) as subquery
        """
        return normalized
    
    def create_comparable_queries(self, query1: str, query2: str) -> Tuple[str, str]:
        """Create two queries that can be compared using set operations"""
        meta1 = self.get_query_metadata(query1)
        meta2 = self.get_query_metadata(query2)
        
        # Get union of all columns
        all_columns = list(set(meta1['column_names'] + meta2['column_names']))
        all_columns.sort()  # Consistent ordering
        
        # Normalize both queries
        norm_query1 = self.normalize_query_results(query1, all_columns)
        norm_query2 = self.normalize_query_results(query2, all_columns)
        
        return norm_query1, norm_query2, all_columns
    
    def row_to_hash(self, row: tuple) -> str:
        """Convert a row to a hash for comparison (handles NULLs)"""
        # Convert None to a special string to handle NULLs consistently
        normalized_row = tuple('__NULL__' if x is None else str(x) for x in row)
        return hashlib.md5(str(normalized_row).encode()).hexdigest()
    
    def compare_queries_detailed(self, query1: str, query2: str) -> Dict[str, Any]:
        """Comprehensive comparison of two SQL queries"""
        try:
            # Get normalized queries
            norm_query1, norm_query2, common_columns = self.create_comparable_queries(query1, query2)
            
            # Execute queries and get results
            df1 = pd.read_sql_query(norm_query1, self.conn)
            df2 = pd.read_sql_query(norm_query2, self.conn)
            
            # Convert to sets of hashes for comparison
            set1 = {self.row_to_hash(tuple(row)) for row in df1.itertuples(index=False, name=None)}
            set2 = {self.row_to_hash(tuple(row)) for row in df2.itertuples(index=False, name=None)}
            
            # Calculate metrics
            intersection = set1 & set2
            union = set1 | set2
            only_in_1 = set1 - set2
            only_in_2 = set2 - set1
            
            # Similarity metrics
            jaccard_similarity = len(intersection) / len(union) if union else 1.0
            overlap_coefficient = len(intersection) / min(len(set1), len(set2)) if min(len(set1), len(set2)) > 0 else 0.0
            
            results = {
                'query1_count': len(df1),
                'query2_count': len(df2),
                'intersection_count': len(intersection),
                'union_count': len(union),
                'only_in_query1_count': len(only_in_1),
                'only_in_query2_count': len(only_in_2),
                'jaccard_similarity': round(jaccard_similarity, 4),
                'overlap_coefficient': round(overlap_coefficient, 4),
                'common_columns': common_columns,
                'queries_metadata': {
                    'query1': self.get_query_metadata(query1),
                    'query2': self.get_query_metadata(query2)
                }
            }
            
            return results
            
        except Exception as e:
            raise Exception(f"Error comparing queries: {e}")
    
    def get_intersection_data(self, query1: str, query2: str) -> pd.DataFrame:
        """Get the actual intersection data"""
        norm_query1, norm_query2, _ = self.create_comparable_queries(query1, query2)
        
        intersection_query = f"""
        SELECT * FROM ({norm_query1})
        INTERSECT
        SELECT * FROM ({norm_query2})
        """
        
        return pd.read_sql_query(intersection_query, self.conn)
    
    def get_union_data(self, query1: str, query2: str) -> pd.DataFrame:
        """Get the actual union data"""
        norm_query1, norm_query2, _ = self.create_comparable_queries(query1, query2)
        
        union_query = f"""
        SELECT * FROM ({norm_query1})
        UNION
        SELECT * FROM ({norm_query2})
        """
        
        return pd.read_sql_query(union_query, self.conn)
    
    def get_difference_data(self, query1: str, query2: str, which_difference: str = 'query1_only') -> pd.DataFrame:
        """Get records that exist only in one query
        
        Args:
            which_difference: 'query1_only' or 'query2_only'
        """
        norm_query1, norm_query2, _ = self.create_comparable_queries(query1, query2)
        
        if which_difference == 'query1_only':
            diff_query = f"""
            SELECT * FROM ({norm_query1})
            EXCEPT
            SELECT * FROM ({norm_query2})
            """
        else:  # query2_only
            diff_query = f"""
            SELECT * FROM ({norm_query2})
            EXCEPT
            SELECT * FROM ({norm_query1})
            """
        
        return pd.read_sql_query(diff_query, self.conn)

# Example usage
def example_usage():
    # Connect to your database
    conn = sqlite3.connect(':memory:')  # or your database file
    
    # Create sample data for demonstration
    conn.execute("""
    CREATE TABLE users (
        id INTEGER PRIMARY KEY,
        name TEXT,
        age INTEGER,
        department TEXT
    )
    """)
    
    conn.execute("""
    CREATE TABLE employees (
        emp_id INTEGER PRIMARY KEY,
        full_name TEXT,
        age INTEGER,
        dept TEXT,
        salary REAL
    )
    """)
    
    # Insert sample data
    users_data = [(1, 'Alice', 25, 'IT'), (2, 'Bob', 30, 'HR'), (3, 'Charlie', 35, 'IT')]
    employees_data = [(1, 'Alice', 25, 'IT', 50000), (2, 'Bob', 30, 'HR', 45000), (4, 'David', 28, 'Finance', 55000)]
    
    conn.executemany("INSERT INTO users VALUES (?, ?, ?, ?)", users_data)
    conn.executemany("INSERT INTO employees VALUES (?, ?, ?, ?, ?)", employees_data)
    
    # Initialize comparator
    comparator = SQLQueryComparator(conn)
    
    # Define your queries
    query1 = "SELECT id, name, age FROM users WHERE age > 20"
    query2 = "SELECT emp_id as id, full_name as name, age FROM employees WHERE age < 40"
    
    # Compare queries
    comparison_results = comparator.compare_queries_detailed(query1, query2)
    print("Comparison Results:")
    print(json.dumps(comparison_results, indent=2))
    
    # Get intersection data
    intersection_df = comparator.get_intersection_data(query1, query2)
    print("\nIntersection Data:")
    print(intersection_df)
    
    # Get union data
    union_df = comparator.get_union_data(query1, query2)
    print("\nUnion Data:")
    print(union_df)
    
    # Get differences
    only_in_1 = comparator.get_difference_data(query1, query2, 'query1_only')
    only_in_2 = comparator.get_difference_data(query1, query2, 'query2_only')
    
    print("\nOnly in Query 1:")
    print(only_in_1)
    print("\nOnly in Query 2:")
    print(only_in_2)
    
    conn.close()

if __name__ == "__main__":
    example_usage()