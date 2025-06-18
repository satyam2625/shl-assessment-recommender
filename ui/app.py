import streamlit as st
import requests

st.title("SHL Assessment Recommendation Engine")

query = st.text_input("Enter job role or skills:")

if st.button("Recommend"):
    if query:
        try:
            res = requests.get("https://your-api-url.onrender.com/recommend", params={"query": query})

            if res.status_code == 200:
                data = res.json()
                for rec in data["recommendations"]:
                    st.subheader(rec["name"])
                    st.write(", ".join(rec["tags"]))
            else:
                st.error(f"API Error {res.status_code}: {res.text}")

        except requests.exceptions.RequestException as e:
            st.error(f"Request failed: {e}")
