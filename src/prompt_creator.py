from src.database.db_schema import DbSchema
from src.database.db_loader import DatabaseLoader




def create_prompt(db_schema: DbSchema) -> str:
    return f"""
    system:
      # SQL Query Generator Assistant
      
      You are a specialized SQL query generator that creates correct, executable SQL queries based on database schemas and natural language requests.
      
      ## Your Task
      - Analyze the provided database schema
      - Interpret the user's natural language request
      - Generate a precise SQL query that answers the user's question
      - Ensure the query is syntactically correct and optimized
      
      ## Guidelines
      - Use only tables and columns defined in the schema
      - Consider appropriate JOINs when data spans multiple tables
      - Apply proper filtering conditions based on the request
      - Format your response as a valid SQL query
      
      
    
    user:
    The database schema is as follows:
    {db_schema.get_tables_as_md(add_constraints=False)}
    
    # Examples
    Here are some examples of how to generate SQL queries:
    Given the text: "What is the average salary of all players?"
    The SQL query should be: SELECT AVG(salary) FROM players;

    Given the text: "What is the total number of players in the database?"
    The SQL query should be: SELECT COUNT(*) FROM players;

    Given the text: "What is the total number of players in the database?"
    The SQL query should be: SELECT COUNT(*) FROM players;

    Given the text: "What is the total number of players in the database?"
    The SQL query should be: SELECT COUNT(*) FROM players;

    Given the text: "What is the total number of players in the database?"
    The SQL query should be: SELECT COUNT(*) FROM players;

    Given the text: "What is the total number of players in the database?"
    The SQL query should be: SELECT COUNT(*) FROM players;
    
    **Important**: Return the SQL query only, no other text or comments.
    
    # User Request
    """
    
    



if __name__ == "__main__":
    sqlite_path = "/Users/andirexha/Documents/presentations/20.08.2025/db_creation/baseball/baseball.db"
    db_loader = DatabaseLoader(sqlite_path)
    db_schema = DbSchema(db_loader)
    md_str = db_schema.get_tables_as_md(add_constraints=True)
    with open("prompt.txt", "w", encoding="utf-8") as f:
        f.write(create_prompt(md_str))
    
    
#%%

#%%

#%%