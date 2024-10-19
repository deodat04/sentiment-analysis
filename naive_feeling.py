import csv
from nltk.corpus import wordnet

# Fonction pour récupérer les synonymes via WordNet
def get_synonyms(word):
    synonyms = []
    for syn in wordnet.synsets(word):
        for lemma in syn.lemmas():
            synonyms.append(lemma.name())
    return list(set(synonyms))

# Fonction pour analyser un avis et déterminer le sentiment
def analyze_review(review_text, positive_synonyms, negative_synonyms):
    words = review_text.lower().split()

    positive_count = 0
    negative_count = 0

    for word in words:
        if word in positive_synonyms:
            positive_count += 1
        elif word in negative_synonyms:
            negative_count += 1

    if positive_count > negative_count:
        return "Positif"
    elif negative_count > positive_count:
        return "Négatif"
    else:
        return "Neutre"

# Fonction pour analyser un fichier CSV et calculer les résultats
def analyze_csv(input_file, output_file, positive_word, negative_word):
    positive_synonyms = get_synonyms(positive_word)
    negative_synonyms = get_synonyms(negative_word)

    total_positif = 0
    total_negatif = 0
    total_neutre = 0
    total_reviews = 0

    with open(input_file, mode='r', encoding='utf-8') as infile, open(output_file, mode='w', newline='', encoding='utf-8') as outfile:
        reader = csv.DictReader(infile)
        fieldnames = ['id', 'result']
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()

        for row in reader:
            review_text = row['reviews.text'] + " " + row['reviews.title']
            result = analyze_review(review_text, positive_synonyms, negative_synonyms)

            if result == "Positif":
                total_positif += 1
            elif result == "Négatif":
                total_negatif += 1
            else:
                total_neutre += 1

            writer.writerow({'id': row['id'], 'result': result})

            total_reviews += 1

    percent_positif = (total_positif / total_reviews) * 100
    percent_negatif = (total_negatif / total_reviews) * 100
    percent_neutre = (total_neutre / total_reviews) * 100

    print("\n-------------------------------")
    print("|   Proportion des résultats    | POSITIF | NEGATIF | NEUTRE |")
    print("-------------------------------")
    print(f"| Effectifs                       |   {total_positif}     |   {total_negatif}     |   {total_neutre}    |")
    print(f"| Pourcentage                  | {percent_positif:.2f} %  | {percent_negatif:.2f} % | {percent_neutre:.2f} % |")
    print("-------------------------------\n")

    return positive_synonyms, negative_synonyms

def display_synonyms(positive_synonyms, negative_synonyms):
    choice = input("Souhaitez-vous voir la liste des synonymes utilisés pour le test?\n1 : Oui\n2 : Non\nVotre choix : ")
    
    if choice == '1':
        print("\nSynonymes pour les mots positifs :")
        print(", ".join(positive_synonyms))
        print("\nSynonymes pour les mots négatifs :")
        print(", ".join(negative_synonyms))
    else:
        print("Fin du programme.")

input_file = 'ElectronicsReview.csv'
output_file = 'results.csv'
positive_word = 'good'
negative_word = 'bad'

positive_synonyms, negative_synonyms = analyze_csv(input_file, output_file, positive_word, negative_word)

display_synonyms(positive_synonyms, negative_synonyms)
