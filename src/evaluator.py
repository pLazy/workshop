from src.database.db_loader import DatabaseLoader
import json
import os
from pathlib import Path



if __name__ == "__main__":
    db_loader = DatabaseLoader()
    ground_truths = json.load(Path("resources/evaluation/prompt2.json").read_text())
    llm_results = json.load(Path("resources/prompts/prompt2_llm.json").read_text())
    
    
    
    # Function to read JSON file
    def read_json_file(file_path):
        try:
            with open(file_path, 'r') as file:
                data = json.load(file)
                return data
        except FileNotFoundError:
            print(f"Error: File not found at {file_path}")
            return None
        except json.JSONDecodeError:
            print(f"Error: Invalid JSON format in {file_path}")
            return None
        except Exception as e:
            print(f"Error reading JSON file: {str(e)}")
            return None
    with db_loader as db:
        results = db.execute_query("SELECT * FROM player;")
        
        
        
        
    print("Hello, World!")