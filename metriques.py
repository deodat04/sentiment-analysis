import csv

def metriques_csv(gold_standard, result_file):
    nombre_corrects = 0
    total_lignes = 0

    with open(gold_standard, mode='r', encoding='utf-8') as gold, open(result_file, mode='r', encoding='utf-8') as res:
        reader1 = csv.DictReader(gold)
        reader2 = csv.DictReader(res)

        # On lit les deux fichiers ligne par ligne en parallèle
        for row1, row2 in zip(reader1, reader2):
            sentiment_gold = row1['reviews.doRecommend']
            sentiment_result = row2['result']

            total_lignes += 1

            if sentiment_gold == sentiment_result:
                nombre_corrects += 1

    exactitude = nombre_corrects / total_lignes
    print(f"Exactitude globale : {exactitude * 100:.2f}%")
    print(nombre_corrects)
    return nombre_corrects


def analyse_metrique_negatif(gold_standard, result_file):
    # Classe réelle A (avis négatif), classe réelle ¬A (avis positif ou neutre)
    A = 'Négatif'
    NA = ['Positif', 'Neutre']  # Positif et Neutre sont considérés comme ¬A

    VP = 0  # Vrai Positif: Négatif prédit et réel
    FN = 0  # Faux Négatif: Négatif réel mais non prédit
    FP = 0  # Faux Positif: Négatif prédit mais non réel
    VN = 0  # Vrai Négatif: Non négatif prédit et non négatif réel

    with open(gold_standard, mode='r', encoding='utf-8') as gold, open(result_file, mode='r', encoding='utf-8') as res:
        reader1 = csv.DictReader(gold)
        reader2 = csv.DictReader(res)

        for row1, row2 in zip(reader1, reader2):
            row_gold = row1['reviews.doRecommend']
            row_result = row2['result']

            if row_gold == A and row_result == A:
                VP += 1  # Vrai négatif identifié
            elif row_gold == A and row_result in NA:
                FN += 1  # Négatif manqué
            elif row_gold in NA and row_result == A:
                FP += 1  # Fausse alarme négative
            elif row_gold in NA and row_result in NA:
                VN += 1  # Correctement classé comme non négatif

    # Affichage des résultats
    print(f"Vrai Positif (VP) : {VP}")
    print(f"Vrai Négatif (VN) : {VN}")
    print(f"Faux Positif (FP) : {FP}")
    print(f"Faux Négatif (FN) : {FN}")

    # Calcul de l'exactitude avec la formule proposée
    exactitude_negatif = (VP + VN) / (VP + VN + FP + FN)
    print(f"Exactitude sur les avis négatifs : {exactitude_negatif * 100:.2f}%")
    return VP, VN, FP, FN


# Fichiers d'entrée
gold = 'gold_standard.csv'
res = 'results.csv'

# Exécuter les métriques générales
metriques_csv(gold, res)

# Analyser les métriques spécifiques aux avis négatifs
analyse_metrique_negatif(gold, res)
