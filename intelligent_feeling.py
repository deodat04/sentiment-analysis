import pandas as pd
import nltk
import matplotlib.pyplot as plt
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.metrics import precision as eval_precision, recall as eval_recall, f_measure as eval_f_measure

sia = SentimentIntensityAnalyzer()

def load_data(csv_file):
    data = pd.read_csv(csv_file)
    return data

def preprocess_text(text):
    words = nltk.word_tokenize(text)
    stop_words = set(nltk.corpus.stopwords.words('english'))
    words = [word for word in words if word.lower() not in stop_words]
    words = [word.lower() for word in words]
    return " ".join(words)

def analyze_sentiments(texts):
    sentiments = []
    for text in texts:
        sentiment = sia.polarity_scores(text)
        sentiment_label = (
            "Positif" if sentiment['compound'] >= 0.05 else
            "Négatif" if sentiment['compound'] <= -0.05 else
            "Neutre"
        )
        
        sentiment['label'] = sentiment_label
        sentiments.append(sentiment)
    return pd.DataFrame(sentiments)

#métriques de performance
def evaluate_metrics(predictions, references):
    metrics = {}
    for label in ["Positif", "Négatif", "Neutre"]:
        ref_set = set(i for i, ref in enumerate(references) if ref == label)
        pred_set = set(i for i, pred in enumerate(predictions) if pred == label)
        
        precision = eval_precision(ref_set, pred_set) or 0.0
        recall = eval_recall(ref_set, pred_set) or 0.0
        f_measure = eval_f_measure(ref_set, pred_set) or 0.0
        
        metrics[label] = {
            "Précision": precision,
            "Rappel": recall,
            "F-mesure": f_measure
        }
    
    #exactitude globale
    correct = sum(1 for ref, pred in zip(references, predictions) if ref == pred)
    accuracy = correct / len(predictions) if predictions else 0
    
    metrics["Exactitude Globale"] = accuracy
    return metrics

#Visualisation des sentiments sous forme d'histogrammes
def plot_histograms(sentiments_df):
    plt.figure(figsize=(10, 6))
    plt.hist(sentiments_df['compound'], bins=30)
    plt.xlabel("Polarité Compound")
    plt.ylabel("Fréquence")
    plt.title("Distribution des sentiments (Polarité Compound)")
    plt.savefig("hist_sentiments.png")
    
    sentiments_count = sentiments_df['label'].value_counts()
    sentiments_count.plot(kind='bar', color=['green', 'red', 'blue'])
    plt.title("Proportion des sentiments")
    plt.xlabel("Sentiment")
    plt.ylabel("Nombre total")
    plt.savefig("proportion_sentiments.png")
    
    grouped_sentiments = sentiments_df.groupby(['product_id', 'label']).size().unstack(fill_value=0).reindex(columns=["Positif", "Négatif", "Neutre"], fill_value=0)
    for product_id, sentiment_data in grouped_sentiments.iterrows():
        sentiment_data.plot(kind='bar', color=['green', 'red', 'blue'])
        plt.title(f"Proportion des sentiments pour le produit ID: {product_id}")
        plt.xlabel("Sentiment")
        plt.ylabel("Nombre total")
        plt.xticks(rotation=0)
        
        plt.savefig(f"sentiments_produit_{product_id}.png")

reviews_df = load_data("ElectronicsReview.csv")
gold_standard_df = load_data("gold_standard.csv")

reviews_df['cleaned_text'] = reviews_df['reviews.text'].fillna('') + ' ' + reviews_df['reviews.title'].fillna('')
reviews_df['cleaned_text'] = reviews_df['cleaned_text'].apply(preprocess_text)

#Analyse sentiments et création du DataFrame des sentiments
sentiments_df = analyze_sentiments(reviews_df['cleaned_text'])
sentiments_df['product_id'] = gold_standard_df['id']  # Associer les IDs des produits

references = gold_standard_df['reviews.doRecommend']
predicted_sentiments = sentiments_df['label'].tolist()
metrics = evaluate_metrics(predicted_sentiments, references)

print("Résultats des métriques par classe:")
for sentiment_class, scores in metrics.items():
    if sentiment_class != "Exactitude Globale":
        print(f"\nClasse {sentiment_class}:")
        print(f"Précision : {scores['Précision'] * 100:.2f}")
        print(f"Rappel : {scores['Rappel'] * 100:.2f}")
        print(f"F-mesure : {scores['F-mesure'] * 100:.2f}")
    else:
        print(f"\n{sentiment_class} : {scores * 100 :.2f}")

plot_histograms(sentiments_df)




#V0
""" 
import pandas as pd
import nltk
import matplotlib.pyplot as plt
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.metrics import f_measure as eval_f_measure
from nltk.metrics import precision as eval_precision
from nltk.metrics import recall as eval_recall
from nltk.classify.util import accuracy as eval_accuracy
from collections import defaultdict

sia = SentimentIntensityAnalyzer()

def load_data(csv_file):
    data = pd.read_csv(csv_file)
    return data

# 2. Traitement des données
def preprocess_text(text):
    words = nltk.word_tokenize(text)
    stop_words = set(nltk.corpus.stopwords.words('english'))
    words = [word for word in words if word.lower() not in stop_words]
    words = [word.lower() for word in words]
    return " ".join(words)

#Appliquer l'analyse de sentiment avec VADER
def analyze_sentiments(texts):
    sentiments = []
    for text in texts:
        sentiment = sia.polarity_scores(text)
        sentiments.append(sentiment)
    return sentiments

#Visualisation des sentiments sous forme d'histogrammes
def plot_histograms(sentiments_df):
    #Hist1: Distribution des avis pour chaque utilisateur
    plt.figure(figsize=(10, 6))
    plt.hist(sentiments_df['compound'], bins=30)
    plt.xlabel("Polarité Compound")
    plt.ylabel("Fréquence")
    plt.title("Distribution des sentiments (Polarité Compound)")
    plt.savefig("hist_sentiments.png")
    plt.show()

    #Hist2: Proportions des sentiments (Positif, Négatif, Neutre)
    sentiments_count = sentiments_df[['pos', 'neg', 'neu']].sum()
    sentiments_count.plot(kind='bar', color=['green', 'red', 'blue'])
    plt.title("Proportion des sentiments")
    plt.xlabel("Sentiment")
    plt.ylabel("Nombre total")
    plt.savefig("proportion_sentiments.png")
    plt.show()

def calculate_metrics(sentiments_df, actual_labels):
    predicted_labels = []
    
    actual_labels = actual_labels.fillna("NEUTRAL").astype(str)
    actual_labels = actual_labels.replace({"TRUE": "TRUE", "FALSE": "FALSE", "": "NEUTRAL"})

    #Prédiction des labels en fonction du score compound
    for _, row in sentiments_df.iterrows():
        if row['compound'] >= 0.3:
            predicted_labels.append("TRUE")
        elif row['compound'] <= -0.3:
            predicted_labels.append("FALSE")
        else:
            predicted_labels.append("NEUTRAL")


    #Vérification de la distribution des labels
    print("Distribution des prédictions : ", pd.Series(predicted_labels).value_counts())
    print("Distribution des labels réels : ", actual_labels.value_counts())

    
    test_set = list(zip(predicted_labels, actual_labels))
    
    # Dictionnaires pour les scores dorés et observés
    gold_results = defaultdict(set)
    test_results = defaultdict(set)
    labels = set()

    # Calcul des labels pour chaque classe
    for i, (predicted, actual) in enumerate(test_set):
        labels.add(actual)
        gold_results[actual].add(i)
        test_results[predicted].add(i)
    
    # Calcul des métriques pour chaque sentiment
    metrics_results = {}
    for label in labels:
        precision_score = eval_precision(gold_results[label], test_results[label]) or 0.0
        recall_score = eval_recall(gold_results[label], test_results[label]) or 0.0
        f_measure_score = eval_f_measure(gold_results[label], test_results[label]) or 0.0
        
        metrics_results[f"Precision [{label}]"] = precision_score
        metrics_results[f"Recall [{label}]"] = recall_score
        metrics_results[f"F-measure [{label}]"] = f_measure_score
    
    # Calcul de l'exactitude globale
    accuracy_score = sum(1 for (pred, actual) in test_set if pred == actual) / len(actual_labels)
    metrics_results["Accuracy"] = accuracy_score
    
    # Affichage des résultats
    print(f"Exactitude globale : {accuracy_score * 100:.2f}%")
    for sentiment in labels:
        print(f"{sentiment} - Précision : {metrics_results[f'Precision [{sentiment}]'] * 100:.2f}%")
        print(f"{sentiment} - Rappel : {metrics_results[f'Recall [{sentiment}]'] * 100:.2f}%")
        print(f"{sentiment} - F-mesure : {metrics_results[f'F-measure [{sentiment}]'] * 100:.2f}%")
    
    return metrics_results

def main():
    # Charger le fichier CSV
    csv_file = "ElectronicsReview.csv" 
    data = load_data(csv_file)

    data['processed_text'] = data['reviews.text'].fillna('') + ' ' + data['reviews.title'].fillna('')
    data['processed_text'] = data['processed_text'].apply(preprocess_text)

    sentiments = analyze_sentiments(data['processed_text'])
    sentiments_df = pd.DataFrame(sentiments)

    plot_histograms(sentiments_df)

    if 'reviews.doRecommend' in data.columns:
        calculate_metrics(sentiments_df, data['reviews.doRecommend'])
    else:
        print("La colonne 'reviews.doRecommend' est absente, les métriques ne peuvent pas être calculées.")

if __name__ == "__main__":
    main()
 """