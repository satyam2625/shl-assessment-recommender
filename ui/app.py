# ui/app.py

import streamlit as st
import requests

st.title("SHL Assessment Recommendation Engine")

query = st.text_input("Enter job role or skills:")

if st.button("Recommend"):
    if query:
        res = requests.get("https://your-fastapi-app.onrender.com/recommend", params={"query": query})
        for rec in res.json()["recommendations"]:
            st.subheader(rec["name"])
            st.write(", ".join(rec["tags"]))
