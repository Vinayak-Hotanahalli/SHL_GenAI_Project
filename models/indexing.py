from sentence_transformers import SentenceTransformer
import faiss, numpy as np, pandas as pd, pickle
from sklearn.feature_extraction.text import TfidfVectorizer
import scipy.sparse as sp
from pathlib import Path

Path("indexes").mkdir(exist_ok=True)

df = pd.read_csv("data/shl_catalog_clean.csv")
corpus = (df["name"].fillna("") + ". " + df["description"].fillna("")).tolist()

model = SentenceTransformer("all-MiniLM-L6-v2")
emb = model.encode(corpus, show_progress_bar=True, convert_to_numpy=True, normalize_embeddings=True)

index = faiss.IndexFlatIP(emb.shape[1])
index.add(emb)
faiss.write_index(index, "indexes/faiss.index")

np.save("indexes/embeddings.npy", emb)
pickle.dump(df.to_dict(orient="records"), open("indexes/catalog.pkl","wb"))

vectorizer = TfidfVectorizer(stop_words="english", ngram_range=(1,2), max_features=20000)
X = vectorizer.fit_transform(corpus)
sp.save_npz("indexes/tfidf.npz", X)
pickle.dump(vectorizer, open("indexes/tfidf_vectorizer.pkl","wb"))
print("✅ Indexing complete!")
