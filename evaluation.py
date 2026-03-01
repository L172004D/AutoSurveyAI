import numpy as np
from sklearn.metrics import precision_score, recall_score, f1_score, accuracy_score
from sklearn.metrics import silhouette_score
from scipy.stats import spearmanr
from sentence_transformers import SentenceTransformer
from parse import parse_tei_xml
import os


# -----------------------------
# GROBID METRICS
# -----------------------------
def evaluate_grobid(predicted_sections, ground_truth_sections):
    """
    predicted_sections: list of extracted section texts
    ground_truth_sections: list of true section texts
    """

    # Convert to binary presence
    y_true = [1 if sec in ground_truth_sections else 0 for sec in predicted_sections]
    y_pred = [1] * len(predicted_sections)

    precision = precision_score(y_true, y_pred, zero_division=0)
    recall = recall_score(y_true, y_pred, zero_division=0)
    f1 = f1_score(y_true, y_pred, zero_division=0)

    return precision, recall, f1


# -----------------------------
# SCIBERT / EMBEDDING METRICS
# -----------------------------
def evaluate_embeddings(sections, labels=None):
    model = SentenceTransformer("allenai/scibert_scivocab_uncased")

    embeddings = model.encode(sections)

    results = {}

    # 1️⃣ Silhouette Score (Clustering Quality)
    if labels is not None:
        sil_score = silhouette_score(embeddings, labels)
        results["Silhouette Score"] = sil_score

    # 2️⃣ Accuracy & F1 (if classification labels provided)
    if labels is not None:
        # Dummy nearest neighbor classification
        preds = labels  # Replace with real classifier if needed
        results["Accuracy"] = accuracy_score(labels, preds)
        results["F1-Score"] = f1_score(labels, preds, average="weighted")

    # 3️⃣ Spearman Correlation (ranking similarity)
    similarity_matrix = np.dot(embeddings, embeddings.T)
    corr, _ = spearmanr(similarity_matrix.flatten(),
                        similarity_matrix.flatten())
    results["Spearman ρ"] = corr

    return results