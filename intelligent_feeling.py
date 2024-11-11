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

#sentiments sous forme d'histogrammes
def plot_histograms(sentiments_df):
    #proportion des sentiments par avis
    plt.figure(figsize=(10, 6))
    plt.hist(sentiments_df['compound'], bins=30)
    plt.xlabel("Polarité Compound")
    plt.ylabel("Fréquence")
    plt.title("Distribution des sentiments (Polarité Compound)")
    plt.savefig("hist_sentiments.png")
    plt.close()
    
    #proportion des sentiments globaux
    sentiments_count = sentiments_df['label'].value_counts()
    sentiments_count.plot(kind='bar', color=['green', 'red', 'blue'])
    plt.title("Proportion des sentiments")
    plt.xlabel("Sentiment")
    plt.ylabel("Nombre total")
    plt.savefig("proportion_sentiments.png")
    plt.close()
    
    #proportion des sentiments pour chaque produit
    grouped_sentiments = sentiments_df.groupby(['product_id', 'label']).size().unstack(fill_value=0).reindex(columns=["Positif", "Négatif", "Neutre"], fill_value=0)
    
    for product_id, sentiment_data in grouped_sentiments.iterrows():
        plt.figure(figsize=(8, 6))
        sentiment_data.plot(kind='bar', color=['green', 'red', 'blue'])
        plt.title(f"Proportion des sentiments pour le produit ID: {product_id}")
        plt.xlabel("Sentiment")
        plt.ylabel("Nombre total")
        plt.xticks(rotation=0)
        
        plt.savefig(f"sentiments_produit_{product_id}.png")
        plt.close()


reviews_df = load_data("ElectronicsReview.csv")
gold_standard_df = load_data("gold_standard.csv")

reviews_df['cleaned_text'] = reviews_df['reviews.text'].fillna('') + ' ' + reviews_df['reviews.title'].fillna('')
reviews_df['cleaned_text'] = reviews_df['cleaned_text'].apply(preprocess_text)

sentiments_df = analyze_sentiments(reviews_df['cleaned_text'])
sentiments_df['product_id'] = gold_standard_df['id']  #associer id du produit

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


def evaluate_metrics_per_product(predictions, references, product_ids):
    product_metrics = {}

    #regrouper les prédictions et les références par produit
    for product_id in set(product_ids):
        product_pred = [pred for pred, pid in zip(predictions, product_ids) if pid == product_id]
        product_ref = [ref for ref, pid in zip(references, product_ids) if pid == product_id]

        #métriques pour ce produit
        metrics = {}
        for label in ["Positif", "Négatif", "Neutre"]:
            ref_set = set(i for i, ref in enumerate(product_ref) if ref == label)
            pred_set = set(i for i, pred in enumerate(product_pred) if pred == label)

            precision = eval_precision(ref_set, pred_set) or 0.0
            recall = eval_recall(ref_set, pred_set) or 0.0
            f_measure = eval_f_measure(ref_set, pred_set) or 0.0

            metrics[label] = {
                "Précision": precision,
                "Rappel": recall,
                "F-mesure": f_measure
            }
        
        #exactitude pour ce produit
        correct = sum(1 for ref, pred in zip(product_ref, product_pred) if ref == pred)
        accuracy = correct / len(product_pred) if product_pred else 0

        metrics["Exactitude Globale"] = accuracy
        product_metrics[product_id] = metrics

    return product_metrics

predicted_sentiments = sentiments_df['label'].tolist()  
references = gold_standard_df['reviews.doRecommend'].tolist() 

product_metrics = evaluate_metrics_per_product(predicted_sentiments, references, sentiments_df['product_id'].tolist())

for product_id, metrics in product_metrics.items():
    print(f"\nProduit ID: {product_id}")
    for sentiment_class, scores in metrics.items():
        if sentiment_class != "Exactitude Globale":
            print(f"\nClasse {sentiment_class}:")
            print(f"Précision : {scores['Précision'] * 100:.2f}")
            print(f"Rappel : {scores['Rappel'] * 100:.2f}")
            print(f"F-mesure : {scores['F-mesure'] * 100:.2f}")
        else:
            print(f"\n{sentiment_class} : {scores * 100 :.2f}")


plot_histograms(sentiments_df)