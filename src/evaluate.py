from src.database.db_loader import DatabaseLoader
import json
import os
from pathlib import Path


def get_sql_jaccard_similarity(db, gt_sql, llm_sql):
    # First, let's get the column count of both queries
    # We'll use a simpler approach that doesn't rely on INTERSECT/UNION with different column counts
    
    # Get the results of both queries
    try:
        gt_results = db.execute_query(gt_sql)
        llm_results = db.execute_query(llm_sql)
        
        # Convert results to sets of tuples for comparison
        # Handle different column structures by converting to string representation
        gt_set = set()
        for row in gt_results:
            # Convert row values to a tuple of strings for comparison
            for (key, value) in row.items():
                gt_set.add((key, value))
        
        llm_set = set()
        for row in llm_results:
            # Convert row values to a tuple of strings for comparison
            for (key, value) in row.items():
                llm_set.add((key, value))
        
        #print(gt_set)
        #print(llm_set)
        # Calculate Jaccard similarity
        intersection_size = len(gt_set.intersection(llm_set))
        print(intersection_size)
        union_size = len(gt_set.union(llm_set))
        print(union_size)
        if union_size == 0:
            return 0.0
        
        jaccard_similarity = intersection_size / union_size
        return jaccard_similarity
        
    except Exception as e:
        print(f"Error calculating Jaccard similarity: {e}")
        return None

if __name__ == "__main__":
    sqlite_path = "/Users/andirexha/Documents/presentations/20.08.2025/db_creation/baseball/baseball.db"
    db_loader = DatabaseLoader(sqlite_path)
    p = Path("resources/evaluation/examples_queries_test.json")
    text = p.read_text()
    ground_truths = json.loads(text)
    p = Path("resources/evaluation/generated_queries.json")
    text = p.read_text()
    llm_results = json.loads(text)
    
    with db_loader as db:
        for i in range(len(ground_truths)):
            current_gt = ground_truths[i]
            current_llm = llm_results[i]            
            current_gt_sql = current_gt["sql"]
            current_llm_sql = current_llm["sql"]
            print(current_gt_sql)
            print(current_llm_sql)
            print(get_sql_jaccard_similarity(db, current_gt_sql, current_llm_sql))
            print("--------------------------------")
            