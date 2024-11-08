import csv

def metriques_csv(gold_standard, result_file):
    nombre_corrects = 0
    total_lignes = 0

    with open(gold_standard, mode='r', encoding='utf-8') as gold, open(result_file, mode='r', encoding='utf-8') as res:
        reader1 = csv.DictReader(gold)
        reader2 = csv.DictReader(res)

        for row1, row2 in zip(reader1, reader2):
            sentiment_gold = row1['reviews.doRecommend']
            sentiment_result = row2['result']

            total_lignes += 1

            if sentiment_gold == sentiment_result:
                nombre_corrects += 1

    exactitude = nombre_corrects / total_lignes
    print("Nombre elements correct", nombre_corrects)
    print(f"Exactitude globale : {exactitude * 100:.2f}%")
    return nombre_corrects


def analyse_metrique_negatif(gold_standard, result_file):
    # Classe réelle A (avis négatif), classe réelle ¬A (avis positif ou neutre)
    A = 'Négatif'
    NA = ['Positif', 'Neutre']

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

    print(f"Vrai Positif (VP) : {VP}")
    print(f"Vrai Négatif (VN) : {VN}")
    print(f"Faux Positif (FP) : {FP}")
    print(f"Faux Négatif (FN) : {FN}")

    exactitude_negatif = (VP + VN) / (VP + VN + FP + FN)
    precision_negatif = VP / (VP + FP)
    rappel_negatif = VP / (VP + FN)
    f_mesure_negatif = 2 * ((precision_negatif * rappel_negatif) / (precision_negatif + rappel_negatif))
    print(f"Exactitude sur les avis négatifs : {exactitude_negatif * 100:.2f}%")
    print(f"Précision sur les avis négatifs : {precision_negatif * 100:.2f}%")
    print(f"Rappel sur les avis négatifs : {rappel_negatif * 100:.2f}%")
    print(f"F-mesure sur les avis négatifs : {f_mesure_negatif * 100:.2f}%")

    return VP, VN, FP, FN


def analyse_metrique_positif(gold_standard, result_file):
    # Classe réelle A (avis positif), classe réelle ¬A (avis negatif ou neutre)
    A = 'Positif'
    NA = ['Négatif', 'Neutre']

    VP = 0  
    FN = 0  
    FP = 0  
    VN = 0  

    with open(gold_standard, mode='r', encoding='utf-8') as gold, open(result_file, mode='r', encoding='utf-8') as res:
        reader1 = csv.DictReader(gold)
        reader2 = csv.DictReader(res)

        for row1, row2 in zip(reader1, reader2):
            row_gold = row1['reviews.doRecommend']
            row_result = row2['result']

            if row_gold == A and row_result == A:
                VP += 1  
            elif row_gold == A and row_result in NA:
                FN += 1 
            elif row_gold in NA and row_result == A:
                FP += 1  
            elif row_gold in NA and row_result in NA:
                VN += 1  

    print(f"Vrai Positif (VP) : {VP}")
    print(f"Vrai Négatif (VN) : {VN}")
    print(f"Faux Positif (FP) : {FP}")
    print(f"Faux Négatif (FN) : {FN}")

    exactitude_positif = (VP + VN) / (VP + VN + FP + FN)
    precision_positif = VP / (VP + FP)
    rappel_positif = VP / (VP + FN)
    f_mesure_positif = 2 * ((precision_positif * rappel_positif) / (precision_positif + rappel_positif))
    print(f"Exactitude sur les avis positifs : {exactitude_positif * 100:.2f}%")
    print(f"Précision sur les avis positifs : {precision_positif * 100:.2f}%")
    print(f"Rappel sur les avis positifs : {rappel_positif * 100:.2f}%")
    print(f"F-mesure sur les avis positifs : {f_mesure_positif * 100:.2f}%")
    return VP, VN, FP, FN



def analyse_metrique_neutre(gold_standard, result_file):
    # Classe réelle A (avis neutre), classe réelle ¬A (avis positif ou négatif)
    A = 'Neutre'
    NA = ['Positif', 'Négatif']

    VP = 0  
    FN = 0  
    FP = 0  
    VN = 0  

    with open(gold_standard, mode='r', encoding='utf-8') as gold, open(result_file, mode='r', encoding='utf-8') as res:
        reader1 = csv.DictReader(gold)
        reader2 = csv.DictReader(res)

        for row1, row2 in zip(reader1, reader2):
            row_gold = row1['reviews.doRecommend']
            row_result = row2['result']

            if row_gold == A and row_result == A:
                VP += 1  
            elif row_gold == A and row_result in NA:
                FN += 1 
            elif row_gold in NA and row_result == A:
                FP += 1 
            elif row_gold in NA and row_result in NA:
                VN += 1 

    print(f"Vrai Positif (VP) : {VP}")
    print(f"Vrai Négatif (VN) : {VN}")
    print(f"Faux Positif (FP) : {FP}")
    print(f"Faux Négatif (FN) : {FN}")

    exactitude_neutre = (VP + VN) / (VP + VN + FP + FN)
    precision_neutre = VP / (VP + FP)
    rappel_neutre = VP / (VP + FN)
    f_mesure_neutre = 2 * ((precision_neutre * rappel_neutre) / (precision_neutre + rappel_neutre))
    print(f"Exactitude sur les avis neutres : {exactitude_neutre * 100:.2f}%")
    print(f"Précision sur les avis neutres : {precision_neutre * 100:.2f}%")
    print(f"Rappel sur les avis neutres : {rappel_neutre * 100:.2f}%")
    print(f"F-mesure sur les avis neutres : {f_mesure_neutre * 100:.2f}%")
    return VP, VN, FP, FN



def analyse_metrique_products(gold_standard, result_file):

    id_products ['AVpf3txeLJeJML43FN82', 'AVphzgbJLJeJML43fA0o', 'AV1YFmcQglJLPUi8IGd1', 'AWIm0C3TYSSHbkXwx3S6', 'AVpfnp8HLJeJML43AmVi',
    'AVpgF1BOilAPnD_xnTsK', 'AVpiUMISilAPnD_xC-hu', 'AVpe8ZRY1cnluZ0-aY4H', 'AVpfnuDailAPnD_xfKZY', 'AVpgfP3DilAPnD_xtG3M',
    'AVpe7vI_ilAPnD_xRMq2', 'AVpgGPyq1cnluZ0-wbTJ', 'AVphUeKeilAPnD_x3-Be', 'AVqlHaLknnc1JgDc3m5y'
    ]

    metrics_by_product = {product_id: {"VP": 0, "VN": 0, "FP": 0, "FN": 0} for product_id in id_products}

    with open(gold_standard, mode='r', encoding='utf-8') as gold, open(result_file, mode='r', encoding='utf-8') as res:
        reader1 = csv.DictReader(gold)
        reader2 = csv.DictReader(res)

        for row1, row2 in zip(reader1, reader2):
            product_id = row1['id']
            if product_id in id_products:
                sentiment_gold = row1['reviews.doRecommend']
                sentiment_result = row2['result']

                if sentiment_gold == 'positive' and sentiment_result == 'positive':
                    metrics_by_product[product_id]['VP'] += 1
                elif sentiment_gold == 'negative' and sentiment_result == 'negative':
                    metrics_by_product[product_id]['VN'] += 1
                elif sentiment_gold == 'positive' and sentiment_result == 'negative':
                    metrics_by_product[product_id]['FN'] += 1
                elif sentiment_gold == 'negative' and sentiment_result == 'positive':
                    metrics_by_product[product_id]['FP'] += 1

    #affichage des métriques pour chaque produit
    for product_id, metrics in metrics_by_product.items():
        VP = metrics['VP']
        VN = metrics['VN']
        FP = metrics['FP']
        FN = metrics['FN']
        
        precision = VP / (VP + FP) if (VP + FP) > 0 else 0
        rappel = VP / (VP + FN) if (VP + FN) > 0 else 0
        f_mesure = 2 * ((precision * rappel) / (precision + rappel)) if (precision + rappel) > 0 else 0

        print(f"Produit {product_id} :")
        print(f"  Vrai Positif (VP) : {VP}")
        print(f"  Vrai Négatif (VN) : {VN}")
        print(f"  Faux Positif (FP) : {FP}")
        print(f"  Faux Négatif (FN) : {FN}")
        print(f"  Précision : {precision:.2f}")
        print(f"  Rappel : {rappel:.2f}")
        print(f"  F-mesure : {f_mesure:.2f}\n")

gold = 'gold_standard.csv'
res = 'results.csv'

metriques_csv(gold, res)

analyse_metrique_negatif(gold, res)
print('\n')
analyse_metrique_positif(gold, res)
print('\n')
analyse_metrique_neutre(gold, res)