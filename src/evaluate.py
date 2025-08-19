from src.database.db_loader import DatabaseLoader
import json
import os
from pathlib import Path
import pandas as pd
from difflib import SequenceMatcher


def get_dfs(db, gt_query, llm_query):
    gt_results = db.execute_query(gt_query)
    llm_results = db.execute_query(llm_query)
    gt_df = pd.DataFrame(gt_results)
    llm_df = pd.DataFrame(llm_results)
    mapping = get_column_mapping(llm_df.columns, gt_df.columns)
    llm_df = get_df_with_mapped_columns(llm_df, mapping)
    return gt_df, llm_df

def get_column_mapping(source_columns: list, target_columns: list, threshold: float = 0.7):
    """
    Returns a mapping of source columns to target columns.
    This can be better implemented using a sql parser, and checking the column names in the select statement.
    """
    mapping = {}
    for c1 in source_columns:
        if c1 in target_columns:
            mapping[c1] = c1
        else:
            best_match = max(target_columns, key=lambda c2: SequenceMatcher(None, c1, c2).ratio())
            if SequenceMatcher(None, c1, best_match).ratio() > threshold:
                mapping[c1] = best_match
    return mapping


def get_df_with_mapped_columns(df, mapping):
    """
    Returns a dataframe with the columns mapped to the target columns.
    """
    return df.rename(columns=mapping)

def get_found_elems(source_df, target_df):
    """
    Returns the number of elements in target_df that are also in source_df divided by the number of elements in target_df.
    """
    target_columns = set(target_df.columns)
    common_columns = set(target_df.columns).intersection(set(source_df.columns))
    if common_columns != target_columns:
        return 0
    else:
        target_list = list(map(tuple, target_df.itertuples(index=False)))
        if len(target_list) == 0:
            return 0
        source_list = list(map(tuple, source_df[target_df.columns].itertuples(index=False)))
        
        source_set = set(source_list)
        
        # Count matching rows (considering duplicates)
        matching_rows_count = sum(1 for row in target_list if row in source_set)
        return matching_rows_count/len(target_list)


def get_precision_recall(gt_df, llm_df):
    precision = get_found_elems(gt_df, llm_df)
    recall = get_found_elems(llm_df, gt_df)
    return precision, recall 



def get_jaccard_similarity(gt_df, llm_df):
    try:
        common_columns = list(set(gt_df.columns).intersection(set(llm_df.columns)))
        all_columns = list(set(gt_df.columns).union(set(llm_df.columns)))
        gt_common = gt_df[common_columns]
        llm_common = llm_df[common_columns]
        
        gt_list = list(map(tuple, gt_common.itertuples(index=False)))
        llm_list = list(map(tuple, llm_common.itertuples(index=False)))
        
        gt_set = set(gt_list)
        llm_set = set(llm_list)
        
        # Why not use the intersection of sets or dataframes? because it doesnt work with duplicates
        matching_rows_count = sum(1 for row in gt_list if row in llm_set)
        matching_rows_count_llm = sum(1 for row in llm_list if row in gt_set)

        
        numerator = max(matching_rows_count, matching_rows_count_llm)
        denominator = len(gt_list) * len(all_columns) / len(common_columns) 
        if denominator == 0:
            return 0
        else:
            return numerator / denominator
    except Exception as e:
        return 0
    


if __name__ == "__main__":
    sqlite_path = "/Users/andirexha/Documents/presentations/20.08.2025/db_creation/baseball/baseball.db"
    db_loader = DatabaseLoader(sqlite_path)
    text = Path("resources/evaluation/examples_queries_test.json").read_text()
    ground_truths = json.loads(text)
    text = Path("resources/evaluation/generated_queries.json").read_text()
    llm_results = json.loads(text)
    
    with db_loader as db:
        sum_similarity = 0
        sum_f1_score = 0
        not_executed = 0
        for i in range(len(ground_truths)):
            current_gt = ground_truths[i]
            current_llm = llm_results[i]            
            current_gt_sql = current_gt["query"]
            try:
                current_llm_sql = current_llm["generated_query"]
                gt_df, llm_df = get_dfs(db, current_gt_sql, current_llm_sql)
                jaccard_similarity = get_jaccard_similarity(gt_df, llm_df)
                precision, recall = get_precision_recall(gt_df, llm_df)
            except Exception as e:
                jaccard_similarity = 0
                not_executed += 1
                precision = 0
                recall = 0
                continue
            
            if precision + recall == 0:
                f1_score = 0 
            else:
                f1_score = 2 * (precision * recall) / (precision + recall)
            sum_similarity += jaccard_similarity
            sum_f1_score += f1_score
        print(f"Jaccard Similarity / Partial accuracy: {sum_similarity / len(ground_truths)}")
        print(f"F1 Score: {sum_f1_score / len(ground_truths)}")
        print(f"Not executed: {not_executed}")
        print(f"Total: {len(ground_truths)}")