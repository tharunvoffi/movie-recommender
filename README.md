# 🎬 MovieBot – Semantic Movie Recommendation System

MovieBot is a content-based movie recommender that uses **semantic similarity**
instead of traditional genre-only filtering.

## 🔍 Features
- SBERT-based semantic recommendations
- Genre-based baseline comparison
- Fuzzy title matching
- FAISS for fast similarity search
- Clean UI with loading state
- Flask REST API

## 🧠 Tech Stack
- Python, Flask
- SentenceTransformers (SBERT)
- FAISS
- Scikit-learn
- HTML, CSS, JavaScript

## 🏗 Architecture
User → Flask API → SBERT Embeddings → FAISS Search → Recommendations

## 🚀 Future Improvements
- User feedback loop
- Collaborative filtering
- Cloud deployment (Docker + AWS)
- Evaluation metrics (Precision@K)

## ▶️ Run Locally
```bash
pip install -r requirements.txt
python app.py
