from app.recommender import recommend

def top_k_accuracy(test_cases, catalog, k=3):
    """
    Calculates how often at least one relevant tag is found in the top k recommendations.
    
    test_cases: A list of query strings (e.g., ["python backend", "data analysis"])
    """
    correct = 0
    total = len(test_cases)
    
    if total == 0:
        return 0

    for query in test_cases:
        # Get the recommendations
        recs = recommend(query, k=k, catalog=catalog)
        
        # Collect all tags from the recommended items
        predicted_tags = []
        for r in recs:
            predicted_tags.extend([tag.lower() for tag in r.get("tags", [])])
            
        # Check if any word from the query appears in the predicted tags
        query_terms = query.lower().split()
        if any(term in predicted_tags for term in query_terms):
            correct += 1
            
    return correct / total