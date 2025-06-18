from app.utils import top_k_accuracy
from app.recommender import load_catalog

# Load catalog
catalog = load_catalog()

# Test cases
sample_inputs = [
    "python backend",
    "data analysis",
    "frontend react js"
]

# Evaluate accuracy
accuracy = top_k_accuracy(sample_inputs, catalog, k=3)
print(f"Top-k Accuracy: {accuracy:.2f}")
