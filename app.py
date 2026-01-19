# ================= IMPORTANT FIX =================
import os
os.environ["TRANSFORMERS_NO_TF"] = "1"
# =================================================

from flask import Flask, render_template, request, jsonify
import pandas as pd
import re
import numpy as np

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from rapidfuzz import process, fuzz
import faiss

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "data", "tmdb_5000_movies.csv")
ARTIFACTS_PATH = os.path.join(BASE_DIR, "artifacts")

movies = pd.read_csv(DATA_PATH)[["title", "overview", "genres"]]
movies.fillna("", inplace=True)

STOPWORDS = {"the", "a", "an"}

def normalize_title(text):
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s]", "", text)
    return " ".join(w for w in text.split() if w not in STOPWORDS)

movies["norm_title"] = movies["title"].apply(normalize_title)
indices = pd.Series(movies.index, index=movies["norm_title"]).drop_duplicates()

embeddings = np.load(os.path.join(ARTIFACTS_PATH, "embeddings.npy"))
faiss_index = faiss.read_index(os.path.join(ARTIFACTS_PATH, "faiss.index"))

tfidf = TfidfVectorizer(stop_words="english")
genre_matrix = tfidf.fit_transform(movies["genres"])

def find_best_match(user_input, threshold=70):
    match = process.extractOne(user_input, indices.index, scorer=fuzz.token_sort_ratio)
    return match[0] if match and match[1] >= threshold else None

def semantic_recommend(norm_title, k=5):
    idx = indices[norm_title]
    _, recs = faiss_index.search(embeddings[idx].reshape(1, -1), k + 1)
    return movies.iloc[recs[0][1:]]["title"].tolist()

def genre_recommend(norm_title, k=5):
    idx = indices[norm_title]
    scores = cosine_similarity(genre_matrix[idx], genre_matrix)[0]
    ranked = sorted(enumerate(scores), key=lambda x: x[1], reverse=True)[1:k+1]
    return [movies.iloc[i]["title"] for i, _ in ranked]

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/recommend", methods=["GET", "POST"])
def recommend():
    if request.method == "GET":
        return render_template("recommend.html")

    data = request.get_json()
    title = data.get("title", "").strip()
    if not title:
        return jsonify({"error": "Enter a movie title"}), 400

    norm = normalize_title(title)
    suggestion = None

    if norm not in indices:
        best = find_best_match(norm)
        if not best:
            return jsonify({"error": "Movie not found"}), 404
        norm = best
        suggestion = movies.iloc[indices[norm]]["title"]

    return jsonify({
        "matched": movies.iloc[indices[norm]]["title"],
        "suggestion": suggestion,
        "semantic": semantic_recommend(norm),
        "genre": genre_recommend(norm)
    })

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/health")
def health():
    return {"status": "ok"}

@app.errorhandler(404)
def not_found(e):
    return render_template("404.html"), 404

if __name__ == "__main__":
    app.run(debug=True)
