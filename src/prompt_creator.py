from src.database.db_schema import DbSchema
from src.database.db_loader import DatabaseLoader




def create_prompt(tables_md: str) -> str:
    return f"""
### System:
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
- Identify the connections between tables based on the name of the columns


### User:
The database schema is as follows:
{tables_md}
# Examples
Here are some examples of how to generate SQL queries:
Given the text: "Show all players that won an award and the college they attended."
The SQL query should be: 
```sql
  SELECT DISTINCT p.name_first || ' ' || p.name_last AS player_name,
      pa.award_id,
      pa.year,
      c.name_full AS college_name
  FROM player_award pa
  JOIN player p ON pa.player_id = p.player_id
  JOIN player_college pc ON pa.player_id = pc.player_id
  JOIN college c ON pc.college_id = c.college_id
  ORDER BY pa.year DESC, player_name 
```


Given the text: "Show Hall of Fame players and their salary for the years they played. The result should be ordered by year."
The SQL query should be: 
```sql
  SELECT p.name_first || ' ' || p.name_last AS player_name,
      s.year,
      s.salary,
      h.inducted
  FROM hall_of_fame h
  JOIN player p ON h.player_id = p.player_id
  JOIN salary s ON p.player_id = s.player_id
  WHERE h.inducted = 'Y'
```

Given the text: "Show which players participated in the All-Star game."
The SQL query should be:

```sql
  SELECT DISTINCT p.name_first || ' ' || p.name_last AS player_name,
       a.league_id
  FROM all_star a
  JOIN player p ON a.player_id = p.player_id
```


Given the text: "List manager names, the award they won, and the team they managed that season."
The SQL query should be: 

```sql
  SELECT p.name_first || ' ' || p.name_last AS manager_name,
        ma.award_id,
        t.name AS team_name,
        ma.year
  FROM manager_award ma
  JOIN manager m ON ma.player_id = m.player_id AND ma.year = m.year
  JOIN team t ON m.team_id = t.team_id AND m.year = t.year
  JOIN player p ON m.player_id = p.player_id
```
    

**Important**: Always return the result as a JSON object with the following keys:
* "description": a short explanation of how the sql is generated
* "sql": → the SQL query itself as a string.

**Example**: 
```json
  {{
  "description": "Select the table 'manager'. Join it with the table 'team'. Filter on the team name to be 'Boston Red Stockings'. Selects the manager first name and last name and concatenate them.",
  "sql": "SELECT m.name_first || ' ' ||mp.name_last AS manager_name FROM manager m JOIN team t ON m.team_id = t.team_id WHERE t.name = 'Boston Red Stockings'"
  }}
```

# User Request
\"\"\" 
{{user_request}}
\"\"\" 
"""
    



if __name__ == "__main__":
    sqlite_path = "/Users/andirexha/Documents/presentations/20.08.2025/db_creation/baseball/baseball.db"
    db_loader = DatabaseLoader(sqlite_path)
    db_schema = DbSchema(db_loader)
    md_str = db_schema.get_tables_info()
    prompt = create_prompt(md_str)
    with open("prompt.md", "w", encoding="utf-8") as f:
        f.write(prompt)
 