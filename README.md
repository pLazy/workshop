# Generation of prompt
## Downloading and preparing the data:

- Downloaded the data from https://www.kaggle.com/datasets/seanlahman/the-history-of-baseball 
- Cloned the https://github.com/benhamner/baseball.git found from the kaggle page
- Modified the code to produce the SQL for creating the database
    - Create a database with the import of the data
    - Create the schema for possible Prompt
    - Create a possible SQL PK and FK:
        - This didn't work, as I there are duplication for those PKs
    - Create database: sqlite3 baseball.db < src/import.sql


## Creating the prompt
- Create a connection to the database
- Read from the schema of the database
- Write down the first version of prompt with the create_prompt.py 
    - Uses the text for the prompt
- Create a second prompt where the changes are just the tables creation SQL



# Evaluation:

Given two sqls queries, the question is, how to get a score about similarities?

Stages:
    - First phases of training:
        - the quality of the model is really bad, thus, the most important is the execution
    - Good quality:
        - Use some form of found data
    - Almost perfect:
        - Order the results the result and check if all the results are the same


## Jackard similarity

First step is to get the columns that are similar to match.

Given two sets, the similarity makes a ratio between the common indentified values and the totality of the matching.


## Precision / Recall / F1

This is a per-row calculation: 
- Precision: as the amount of rows returned from the LLM that are present in the ground truth
- Recall: as the amount of rows returned from the ground truth sql, that are found in the LLM response
- F1: the combination of the previous

Note: If the returned results do not have the same columns, the F1 is 0 as the precision or recall is 0 if that is not the case.



