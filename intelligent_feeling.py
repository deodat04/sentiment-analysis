import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import matplotlib.pyplot as plt

# 1. Collecte des données (à partir d'un fichier .txt)
with open("sad.txt", "r", encoding="utf-8") as file:
    text_data = file.readlines()

# 2. Traitement des données
def preprocess_text(text):
    # Tokenisation
    words = nltk.word_tokenize(text)
    # Suppression des mots vides
    stop_words = set(nltk.corpus.stopwords.words('french'))  # Pour le français
    words = [word for word in words if word not in stop_words]
    # Conversion en minuscules
    words = [word.lower() for word in words]
    return " ".join(words)

# Appliquer le prétraitement à chaque ligne du fichier texte
text_data = [preprocess_text(text) for text in text_data]

# 3. Analyse des sentiments avec VADER
sia = SentimentIntensityAnalyzer()
sentiments = []
for text in text_data:
    sentiment = sia.polarity_scores(text)
    sentiments.append(sentiment)

# Conversion en DataFrame pour une meilleure manipulation
import pandas as pd
sentiments_df = pd.DataFrame(sentiments)

# 4. Visualisation des données
# Histogramme de la polarité compound (score global de sentiment)
plt.hist(sentiments_df['compound'], bins=30)
plt.xlabel("Polarité Compound")
plt.ylabel("Fréquence")
plt.title("Distribution des sentiments")
plt.savefig("sentiments_distribution.png")