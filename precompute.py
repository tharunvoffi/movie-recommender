import pandas as pd
import os
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "data", "tmdb_5000_movies.csv")

movies = pd.read_csv(DATA_PATH)[["title", "overview", "genres"]]
movies.fillna("", inplace=True)

model = SentenceTransformer("all-MiniLM-L6-v2")
embeddings = model.encode(
    movies["overview"].tolist(),
    normalize_embeddings=True
).astype("float32")

faiss_index = faiss.IndexFlatIP(embeddings.shape[1])
faiss_index.add(embeddings)

os.makedirs("artifacts", exist_ok=True)
np.save("artifacts/embeddings.npy", embeddings)
faiss.write_index(faiss_index, "artifacts/faiss.index")

print("✅ Embeddings & FAISS index saved")
