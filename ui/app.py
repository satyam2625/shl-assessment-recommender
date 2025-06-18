import streamlit as st
import requests

st.title("SHL Assessment Recommendation Engine")

query = st.text_input("Enter job role or skills:")

if st.button("Recommend"):
    if query:
        res = requests.post("http://localhost:8000/recommend", json={"query": query})
        recommended = res.json()["recommended_assessment"]
        st.subheader("Recommended Assessment:")
        st.write(recommended["title"])
        st.write("Skills:", ", ".join(recommended["skills"]))
