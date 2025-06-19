import streamlit as st
import requests

st.title("SHL Assessment Recommendation Engine")
query = st.text_input("Enter job role or skills:")

if query:
    try:
        res = requests.post("https://your-backend-url.onrender.com/recommend", json={"query": query})
        recommendations = res.json()["recommendations"]
        for rec in recommendations:
            st.subheader(rec["title"])
            st.write("Tags:", ", ".join(rec["tags"]))
    except Exception as e:
        st.error("Failed to fetch recommendations. Please try again.")

        res = requests.post(
  "https://shl-assessment-recommender.onrender.com/recommend",
  json={"query": query}
)

