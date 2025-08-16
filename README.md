# Downloading and preparing the data:

- Downloaded the data from https://www.kaggle.com/datasets/seanlahman/the-history-of-baseball 
- Cloned the https://github.com/benhamner/baseball.git found from the kaggle page
- Modified the code to produce the SQL for creating the database
    - Create a database with the import of the data
    - Create the schema for possible Prompt
    - Create a possible SQL PK and FK:
        - This didn't work, as I there are duplication for those PKs
    - Create database: sqlite3 baseball.db < src/import.sql


# Creating the prompt
- Create a connection to the database
- Read from the schema of the database
- Write down the first version of prompt with the create_prompt.py 
    - Uses the text for the prompt
- Create a second prompt where the changes are just the tables creation SQL