SHL Assessment Recommendation Engine 🧠

A FastAPI + Sentence Transformers-powered recommendation engine that recommends relevant SHL assessments based on input job roles or skills.

🚀 Live Demo

Live API: Try the API

Live UI: Streamlit App

Features

🔍 Semantic matching with Sentence Transformers

🌐 FastAPI backend for serving recommendations

🖥️ Interactive Streamlit UI for users

📊 Evaluation script using top-k accuracy

🛠️ Run It Locally

1. Prerequisites

Python 3.8+

pip

2. Installation

Clone the repository and install the dependencies:

git clone [https://github.com/satyam2625/shl-assessment-recommender.git](https://github.com/satyam2625/shl-assessment-recommender.git)
cd shl-assessment-recommender
pip install -r requirements.txt


3. Run the Backend (FastAPI)

Open a terminal and run:

uvicorn app.main:app --reload --port 8000


The API will be available at http://127.0.0.1:8000.

4. Run the Frontend (Streamlit)

Open a second, new terminal and run:

streamlit run ui/app.py


The web app will open in your browser at http://localhost:8501.