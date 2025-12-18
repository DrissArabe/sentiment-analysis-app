import pandas as pd
from transformers import pipeline

# Initialisation du modèle

sentiment_model = pipeline(
    "sentiment-analysis",
    model="cardiffnlp/twitter-roberta-base-sentiment-latest"
)

#
#

import re
import unicodedata

def normalize_text(text):
    text = text.lower()
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode("utf-8")
    text = re.sub(r"[^a-zA-Z\s]", "", text)
    return text.strip()

#
#

def sentiment_to_score(text):
    if pd.isna(text) or text.strip() == "" or text.strip() in ["-", "/", ".", "*"]:
        return 0.4999  # neutre

    # Liste de mots-clés négatifs
    negative_keywords = [
        "je n'ai pas",
        "effet secondaire",
        "maux de tête",
        "nausées",
        "courbatures",
        "pas de grand chose"
    ]

    # Liste de mots-clés positifs
    positive_keywords = [
    "très bon produit",
    "de bons résultats",
    "excellent",
    "super efficace",
    "je recommande",
    "satisfait",
    "bonne qualité",
    "très grande amélioration",
    "Bravo",
    "très belle expérience",
    "je suis ravie",
    "bon produit",
    "très efficace"
]


    text_lower = text.lower()

    # Cas négatif → score forcé
    if any(keyword in text_lower for keyword in negative_keywords):
        return 0.2999

    # Sinon, calcul via modèle
    result = sentiment_model(text[:300])[0]
    score = float(f"{result['score']:.4f}")

    # Cas positif → bonus de +0.05
    if any(keyword in text_lower for keyword in positive_keywords):
        score = min(score + 0.05, 1.0)  # on limite à 1.0 max

    return score


def sentiment_category(score):
    if score > 0.65:
        return "Positive"
    elif score <= 0.3:
        return "Negative"
    else:
        return "Neutral"

def sentiment_analysis(df):
    """Analyse un DataFrame avec colonne 'Verbatims' et retourne df enrichi"""
    df["Sentiment_Score"] = df["Verbatims"].apply(sentiment_to_score)
    df["Sentiment_Category"] = df["Sentiment_Score"].apply(sentiment_category)
    return df

