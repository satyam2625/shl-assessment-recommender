import os
import requests
import streamlit as st

# --- Configuration ---
# CRITICAL: Default to your actual deployed Render API URL.
# This fixes the connection error on Streamlit Cloud.
DEFAULT_API_URL = "https://shl-assessment-recommender.onrender.com"

# It will still use localhost if you set the env var locally for testing
API_URL = os.getenv("API_URL", DEFAULT_API_URL)

# --- Page Config ---
st.set_page_config(
    page_title="SHL Assessment Recommender",
    page_icon="🧠",
    layout="centered"
)

# --- Custom CSS for better styling ---
st.markdown("""
    <style>
    .stTextInput > div > div > input {
        font-size: 1.2rem;
    }
    .result-card {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 10px;
    }
    .tag {
        display: inline-block;
        background-color: #e0e0ef;
        padding: 2px 8px;
        border-radius: 12px;
        font-size: 0.9rem;
        margin-right: 5px;
        margin-top: 5px;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🧠 SHL Assessment Recommender")
st.markdown("Enter a **job role** (e.g., *'Data Scientist'*) or **skills** (e.g., *'Python, SQL'*) to get relevant assessment recommendations.")

# --- User Input ---
with st.form("search_form"):
    col1, col2 = st.columns([4, 1])
    with col1:
        query = st.text_input("Job Role / Skills", placeholder="e.g. Frontend React Developer", label_visibility="collapsed")
    with col2:
        submitted = st.form_submit_button("🔍 Find", use_container_width=True)

if submitted:
    if not query.strip():
        st.warning("⚠️ Please enter a job role or skills.")
    else:
        with st.spinner("🤖 Analyzing requirements..."):
            try:
                response = requests.get(f"{API_URL}/recommend", params={"query": query, "k": 5}, timeout=60)
                
                if response.status_code == 200:
                    data = response.json()
                    results = data.get("results", [])
                    
                    if results:
                        st.success(f"✅ Found {len(results)} recommendations:")
                        for item in results:
                            # Use custom HTML for better looking cards
                            tags_html = "".join([f"<span class='tag'>{tag}</span>" for tag in item['tags']])
                            st.markdown(
                                f"""
                                <div class="result-card">
                                    <h3>{item['title']}</h3>
                                    <div>{tags_html}</div>
                                </div>
                                """, 
                                unsafe_allow_html=True
                            )
                    else:
                        st.info("ℹ️ No matching assessments found. Try different keywords.")
                else:
                    st.error(f"❌ API Error {response.status_code}: {response.text}")
                    
            except requests.exceptions.ConnectionError:
                st.error(f"🚨 Connection Error: Could not reach the API at `{API_URL}`.")
                st.markdown("If you are running this locally, make sure the FastAPI backend is running.")
            except Exception as e:
                st.error(f"An unexpected error occurred: {e}")