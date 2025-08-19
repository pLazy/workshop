class DbSchema:
    def __init__(self, db_loader):
        self.db_loader = db_loader



    def get_tables_info(self, is_md: bool = False) -> str:
        md_str = ""
        with self.db_loader as db:
            tables = db.get_tables()
    
            for table in tables:
                # Get table column information
                current_table_info = db.get_table_schema(table['name'])
                
                # Get foreign key information
                foreign_keys = db.get_foreign_keys(table['name'])
                
                fk_dict = {}
                for fk in foreign_keys:
                    if is_md:
                        fk_dict.setdefault(fk['from'], []).append(fk)
                    else:
                        fk_dict.setdefault(fk['from'], []).append(fk)
                
                # Markdown table header
                md_str += f"\n### Table: `{table['name']}`\n"
                if is_md:
                    md_str += "Column Name | Type | Constraints |\n"
                    md_str += "|-------------|------|-------------|\n"
                
                # Rows
                for column in current_table_info:
                    constraints = []
                    if column['pk'] > 0:  
                        constraints.append("PK")
                    if column['name'] in fk_dict:  
                        for fk in fk_dict[column['name']]:
                            fk_info = f"FK → {fk['table']}.{fk['to']}"
                            constraints.append(fk_info)
                    if column['notnull'] == 1:
                        constraints.append("NOT NULL")
                    if is_md:
                        constraint_str = ", ".join(constraints) if constraints else ""
                        md_str += f"| {column['name']} | {column['type']} | {constraint_str} |\n"
                    else:
                        constraint_str = ", ".join(constraints) if constraints else ""
                        md_str += f"{column['name']} ({column['type']}{f' {constraint_str}' if constraint_str else ''}), "
                        
                md_str += "\n\n"
        return md_str

