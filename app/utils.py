from app.recommender import recommend

def top_k_accuracy(true_tags, catalog, k=3):
    correct = 0
    total = len(true_tags)
    for query in true_tags:
        recs = recommend(query, catalog, k)
        predicted_tags = [tag for r in recs for tag in r["tags"]]
        if any(tag in predicted_tags for tag in query.lower().split()):
            correct += 1
    return correct / total

