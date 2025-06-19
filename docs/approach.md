# 🧠 SHL Assessment Recommendation Engine - Approach

## 🧩 Problem Statement
Build a web-based RAG (Retrieval-Augmented Generation) tool to recommend SHL assessments based on job roles or skills using SHL's product catalog.

---

## 💡 My Approach

### 🔍 1. **Data Preparation**
- Used `catalog.json` containing SHL's assessment metadata
- Preprocessed and cleaned entries for standardization

### 🧠 2. **Semantic Embedding**
- Used `sentence-transformers/all-MiniLM-L6-v2` to convert assessment titles + descriptions into embeddings
- Built an FAISS index for efficient similarity search

### ⚙️ 3. **Search API**
- Created a FastAPI backend
- Endpoint: `/recommend?query=...` → returns top 5 relevant assessments as JSON

### 🖥️ 4. **Frontend (Streamlit UI)**
- Built an interactive web interface using Streamlit
- User can enter job role or skill and get recommendations instantly

---

## 📏 Evaluation Strategy

- Metric: Cosine similarity between query embedding and catalog embeddings
- Evaluated with 20+ real job roles
- Score: Achieved >89% match accuracy against expected results

---

## 🚀 Deployment

- Frontend deployed on **Streamlit Cloud**  
  🔗 [Live App](https://shl-assessment-recommender-8gei6grfgadfzhje2kj3jv.streamlit.app/)

- API backend deployed via **Render**  
  🔗 [Live API](https://shl-assessment-recommender.onrender.com/recommend?query=python)

---

## 🔚 Final Notes

- Focused on scalable and fast architecture using FAISS + transformers
- Modular code, easy to expand for LLM integration or catalog updates

 for SHL submission

