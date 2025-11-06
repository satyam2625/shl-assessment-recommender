import os
import requests
import streamlit as st

# Set the API URL. 
# It uses the environment variable 'API_URL' if set (for deployment)
# or defaults to the local FastAPI server.
API_URL = os.getenv("API_URL", "http://127.0.0.1:8000")

# --- Page Configuration ---
st.set_page_config(
    page_title="SHL Assessment Recommender",
    page_icon="🧠",
    layout="centered"
)

st.title("🧠 SHL Assessment Recommender")
st.write("Enter a job role or a list of skills to find the most relevant SHL assessments.")

# --- User Input ---
query = st.text_input(
    "Enter Job Role or Skills (e.g., 'Python Backend', 'React Frontend Developer'):",
    placeholder="Type here..."
)

if st.button("Get Recommendations"):
    if not query:
        st.warning("Please enter a query.")
    else:
        with st.spinner("Analyzing..."):
            try:
                # --- API Call ---
                params = {"query": query, "k": 5}
                resp = requests.get(f"{API_URL}/recommend", params=params, timeout=10)
                resp.raise_for_status()  # Raises an error for bad responses (4xx, 5xx)
                
                data = resp.json()
                results = data.get("results", [])
                
                # --- Display Results ---
                if results:
                    st.success(f"Found {len(results)} recommendations for '{query}':")
                    for item in results:
                        with st.container(border=True):
                            st.subheader(item.get("title"))
                            tags = item.get("tags", [])
                            # Display tags nicely as pills
                            st.write(" ".join(f"`{tag}`" for tag in tags))
                else:
                    st.warning("No recommendations found. Try a different query.")
            
            except requests.exceptions.RequestException as e:
                st.error(f"API Error: Could not connect to the recommender API.")
                st.exception(e)