#%%
# what to improve in the code:
# Check what is the best way to keep the database connection open?
# Check how to get the table names and schema in a better way?
# What is the schema of the table? and what is the catalog


#%%
import sys
import os

# Add the project root directory to the Python path
parent_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "/Users/andirexha/Documents/presentations/20.08.2025/kaggledbqa"))
sys.path.append(parent_path)

#%%
# Get the current path
current_path = os.path.abspath(os.path.dirname(__file__))
print(f"Current path: {current_path}")

#%%


from src.database.db_loader import DatabaseLoader


#%%
#sqlite_path = "/Users/andirexha/Documents/presentations/20.08.2025/kaggledbqa/resources/database/database.sqlite"
sqlite_path = "/Users/andirexha/Documents/presentations/20.08.2025/db_creation/baseball/baseball.db"

db_loader = DatabaseLoader(sqlite_path)

with db_loader as db:
    results = db.execute_query("SELECT * FROM batting LIMIT 10")
    print(f"Number of rows: {len(results)}")
    print(results[0])

#%%

#%%
with db_loader as db:
    results = db.execute_query("SELECT name FROM sqlite_master WHERE type='table';")
    
#%%

results
# %%

# Display table schema with PK and FK information
with db_loader as db:
    for table in results:
        print(f"\n{'='*60}")
        print(f"Table: {table['name']}")
        print(f"{'='*60}")
        
        # Get table column information
        current_table_info = db.execute_query(f"PRAGMA table_info({table['name']});")
        
        # Get foreign key information
        foreign_keys = db.execute_query(f"PRAGMA foreign_key_list({table['name']});")
        fk_dict = {}
        for fk in foreign_keys:
            fk_dict[fk['from']] = fk
        
        # Display column information with PK and FK indicators
        print(f"{'CID':<4} {'Column Name':<20} {'Type':<15} {'Constraints':<30}")
        print(f"{'-'*4} {'-'*20} {'-'*15} {'-'*30}")
        
        for column in current_table_info:
            constraints = []
            if column['pk'] == 1:
                constraints.append("PRIMARY KEY")
            if column['name'] in fk_dict:
                fk_info = f"FK -> {fk_dict[column['name']]['table']}.{fk_dict[column['name']]['to']}"
                constraints.append(fk_info)
            if column['notnull'] == 1:
                constraints.append("NOT NULL")
            
            constraint_str = ", ".join(constraints) if constraints else ""
            
            print(f"{column['cid']:<4} {column['name']:<20} {column['type']:<15} {constraint_str:<30}")
        
        print(f"{'='*60}")
#%%

#%%

#%%
# %%

with db_loader as db:
    for table in results:
        print(f"\n{'='*60}")
        print(f"Table: {table['name']}")
        print(f"{'='*60}")
        
        # Get table column information
        current_table_info = db.execute_query(f"PRAGMA table_info({table['name']});")
        
        # Get foreign key information
        foreign_keys = db.execute_query(f"PRAGMA foreign_key_list({table['name']});")
        fk_dict = {}
        for fk in foreign_keys:
            fk_dict.setdefault(fk['from'], []).append(fk)
        
        # Display column information with PK and FK indicators
        print(f"{'CID':<4} {'Column Name':<20} {'Type':<15} {'Constraints':<30}")
        print(f"{'-'*4} {'-'*20} {'-'*15} {'-'*30}")
        
        for column in current_table_info:
            constraints = []
            if column['pk'] > 0:  # ✅ handle multi-column PKs
                constraints.append("PRIMARY KEY")
            if column['name'] in fk_dict:  # ✅ support multi-column FKs
                for fk in fk_dict[column['name']]:
                    fk_info = f"FK -> {fk['table']}.{fk['to']}"
                    constraints.append(fk_info)
            if column['notnull'] == 1:
                constraints.append("NOT NULL")
            
            constraint_str = ", ".join(constraints) if constraints else ""
            
            print(f"{column['cid']:<4} {column['name']:<20} {column['type']:<15} {constraint_str:<30}")
        
        print(f"{'='*60}")

# %%
with db_loader as db:
    for table in results:
        # Get table column information
        current_table_info = db.execute_query(f"PRAGMA table_info({table['name']});")
        print(current_table_info)
        break
#%%

#%%

#%%

#%%
# %%

with db_loader as db:
    for table in results:
        # Get table column information
        current_table_info = db.execute_query(f"PRAGMA table_info({table['name']});")
        
        # Get foreign key information
        foreign_keys = db.execute_query(f"PRAGMA foreign_key_list({table['name']});")
        fk_dict = {}
        for fk in foreign_keys:
            fk_dict.setdefault(fk['from'], []).append(fk)
        
        # Markdown table header
        print(f"\n### Table: `{table['name']}`\n")
        print("Column Name | Type | Constraints |")
        print("|-------------|------|-------------|")
        
        # Rows
        for column in current_table_info:
            constraints = []
            if column['pk'] > 0:  # multi-column PKs
                constraints.append("PRIMARY KEY")
            if column['name'] in fk_dict:  # multi-column FKs
                for fk in fk_dict[column['name']]:
                    fk_info = f"FK → {fk['table']}.{fk['to']}"
                    constraints.append(fk_info)
            if column['notnull'] == 1:
                constraints.append("NOT NULL")
            
            constraint_str = ", ".join(constraints) if constraints else ""
            
            print(f"| {column['name']} | {column['type']} | {constraint_str} |")

# %%
