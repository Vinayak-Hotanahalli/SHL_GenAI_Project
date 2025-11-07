import faiss, numpy as np, pickle, scipy.sparse as sp
from sentence_transformers import SentenceTransformer
from sklearn.feature_extraction.text import TfidfVectorizer

emb_model = SentenceTransformer("all-MiniLM-L6-v2")
idx = faiss.read_index("indexes/faiss.index")
embs = np.load("indexes/embeddings.npy")
catalog = pickle.load(open("indexes/catalog.pkl","rb"))
tfidf = sp.load_npz("indexes/tfidf.npz")
vectorizer = pickle.load(open("indexes/tfidf_vectorizer.pkl","rb"))

def dense_candidates(query, topk=20):
    q_emb = emb_model.encode([query], normalize_embeddings=True)
    D, I = idx.search(q_emb.astype('float32'), topk)
    return [catalog[i] for i in I[0]]

def lexical_candidates(query, topk=20):
    qv = vectorizer.transform([query])
    scores = (tfidf @ qv.T).toarray().ravel()
    top_idx = np.argsort(-scores)[:topk]
    return [catalog[i] for i in top_idx if scores[i] > 0]

def get_candidates(query, topk=10):
    allc = dense_candidates(query, topk*2) + lexical_candidates(query, topk*2)
    seen, unique = set(), []
    for c in allc:
        if c["url"] not in seen:
            unique.append(c)
            seen.add(c["url"])
    return unique[:topk]
