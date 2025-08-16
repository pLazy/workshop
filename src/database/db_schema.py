class DbSchema:
    def __init__(self, db_loader):
        self.db_loader = db_loader


    def get_tables_as_md(self, add_constraints: bool = True) -> str:
        md_str = ""
        with self.db_loader as db:
            tables = db.execute_query("SELECT name FROM sqlite_master WHERE type='table';")
    
            for table in tables:
                # Get table column information
                current_table_info = db.execute_query(f"PRAGMA table_info({table['name']});")
                
                # Get foreign key information
                foreign_keys = db.execute_query(f"PRAGMA foreign_key_list({table['name']});")
                fk_dict = {}
                for fk in foreign_keys:
                    fk_dict.setdefault(fk['from'], []).append(fk)
                
                # Markdown table header
                md_str += f"\n### Table: `{table['name']}`\n"
                if add_constraints:
                    md_str += "Column Name | Type | Constraints |\n"
                    md_str += "|-------------|------|-------------|\n"
                else:
                    md_str += "Column Name | Type |\n"
                    md_str += "|-------------|------|\n"
                
                # Rows
                for column in current_table_info:
                    constraints = []
                    if add_constraints:
                        if column['pk'] > 0:  # multi-column PKs
                            constraints.append("PRIMARY KEY")
                        if column['name'] in fk_dict:  # multi-column FKs
                            for fk in fk_dict[column['name']]:
                                fk_info = f"FK → {fk['table']}.{fk['to']}"
                                constraints.append(fk_info)
                        if column['notnull'] == 1:
                            constraints.append("NOT NULL")
                        
                        constraint_str = ", ".join(constraints) if constraints else ""
                        
                        md_str += f"| {column['name']} | {column['type']} | {constraint_str} |\n"
                    else:
                        md_str += f"| {column['name']} | {column['type']} |\n"
        return md_str


#%%

#%%

#%%
