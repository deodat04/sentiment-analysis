import csv

def analyse_metrique_products(gold_standard, result_file):
    id_products = [
        'AVpf3txeLJeJML43FN82', 'AVphzgbJLJeJML43fA0o', 'AV1YFmcQglJLPUi8IGd1', 'AWIm0C3TYSSHbkXwx3S6',
        'AVpfnp8HLJeJML43AmVi', 'AVpgF1BOilAPnD_xnTsK', 'AVpiUMISilAPnD_xC-hu', 'AVpe8ZRY1cnluZ0-aY4H',
        'AVpfnuDailAPnD_xfKZY', 'AVpgfP3DilAPnD_xtG3M', 'AVpe7vI_ilAPnD_xRMq2', 'AVpgGPyq1cnluZ0-wbTJ',
        'AVphUeKeilAPnD_x3-Be', 'AVqlHaLknnc1JgDc3m5y'
    ]

    metrics_by_product = {product_id: {"correct": 0, "total": 0} for product_id in id_products}

    with open(gold_standard, mode='r', encoding='utf-8') as gold, open(result_file, mode='r', encoding='utf-8') as res:
        reader1 = csv.DictReader(gold)
        reader2 = csv.DictReader(res)

        for row1, row2 in zip(reader1, reader2):
            product_id = row1['id']
            if product_id in id_products:
                sentiment_gold = row1['reviews.doRecommend']
                sentiment_result = row2['result']

                metrics_by_product[product_id]['total'] += 1

                if sentiment_gold == sentiment_result:
                    metrics_by_product[product_id]['correct'] += 1

    # Affichage des métriques pour chaque produit
    for product_id, metrics in metrics_by_product.items():
        total = metrics['total']
        correct = metrics['correct']
        exactitude = correct / total if total > 0 else 0

        print(f"Produit {product_id} :")
        print(f"  Exactitude : {exactitude * 100:.2f}")

    return metrics_by_product


def analyse_metriques_products_negatif(gold_standard, result_file):
    id_products = [
        'AVpf3txeLJeJML43FN82', 'AVphzgbJLJeJML43fA0o', 'AV1YFmcQglJLPUi8IGd1', 'AWIm0C3TYSSHbkXwx3S6',
        'AVpfnp8HLJeJML43AmVi', 'AVpgF1BOilAPnD_xnTsK', 'AVpiUMISilAPnD_xC-hu', 'AVpe8ZRY1cnluZ0-aY4H',
        'AVpfnuDailAPnD_xfKZY', 'AVpgfP3DilAPnD_xtG3M', 'AVpe7vI_ilAPnD_xRMq2', 'AVpgGPyq1cnluZ0-wbTJ',
        'AVphUeKeilAPnD_x3-Be', 'AVqlHaLknnc1JgDc3m5y'
    ]

    metrics_by_product = {product_id: {"VP": 0, "VN": 0, "FP": 0, "FN": 0} for product_id in id_products}
     
    A = 'Négatif'
    NA = ['Positif', 'Neutre']

    with open(gold_standard, mode='r', encoding='utf-8') as gold, open(result_file, mode='r', encoding='utf-8') as res:
        reader1 = csv.DictReader(gold)
        reader2 = csv.DictReader(res)

        for row1, row2 in zip(reader1, reader2):
            product_id = row1['id']
            if product_id in id_products:
                row_gold = row1['reviews.doRecommend']
                row_result = row2['result']

                if row_gold == A and row_result == A:
                    metrics_by_product[product_id]['VP'] += 1
                elif row_gold == A and row_result in NA:
                    metrics_by_product[product_id]['FN'] += 1
                elif row_gold in NA and row_result == A:
                    metrics_by_product[product_id]['FP'] += 1
                elif row_gold in NA and row_result in NA:
                    metrics_by_product[product_id]['VN'] += 1

    # Affichage des métriques pour chaque produit
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
        print(f"  Précision : {precision * 100:.2f}")
        print(f"  Rappel : {rappel * 100:.2f}")
        print(f"  F-mesure : {f_mesure * 100:.2f}\n")

    return metrics_by_product

def analyse_metriques_products_neutre(gold_standard, result_file):
    id_products = [
        'AVpf3txeLJeJML43FN82', 'AVphzgbJLJeJML43fA0o', 'AV1YFmcQglJLPUi8IGd1', 'AWIm0C3TYSSHbkXwx3S6',
        'AVpfnp8HLJeJML43AmVi', 'AVpgF1BOilAPnD_xnTsK', 'AVpiUMISilAPnD_xC-hu', 'AVpe8ZRY1cnluZ0-aY4H',
        'AVpfnuDailAPnD_xfKZY', 'AVpgfP3DilAPnD_xtG3M', 'AVpe7vI_ilAPnD_xRMq2', 'AVpgGPyq1cnluZ0-wbTJ',
        'AVphUeKeilAPnD_x3-Be', 'AVqlHaLknnc1JgDc3m5y'
    ]

    metrics_by_product = {product_id: {"VP": 0, "VN": 0, "FP": 0, "FN": 0} for product_id in id_products}
     
    A = 'Neutre'
    NA = ['Positif', 'Négatif']

    with open(gold_standard, mode='r', encoding='utf-8') as gold, open(result_file, mode='r', encoding='utf-8') as res:
        reader1 = csv.DictReader(gold)
        reader2 = csv.DictReader(res)

        for row1, row2 in zip(reader1, reader2):
            product_id = row1['id']
            if product_id in id_products:
                row_gold = row1['reviews.doRecommend']
                row_result = row2['result']

                if row_gold == A and row_result == A:
                    metrics_by_product[product_id]['VP'] += 1
                elif row_gold == A and row_result in NA:
                    metrics_by_product[product_id]['FN'] += 1
                elif row_gold in NA and row_result == A:
                    metrics_by_product[product_id]['FP'] += 1
                elif row_gold in NA and row_result in NA:
                    metrics_by_product[product_id]['VN'] += 1

    # Affichage des métriques pour chaque produit
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
        print(f"  Précision : {precision * 100:.2f}")
        print(f"  Rappel : {rappel * 100:.2f}")
        print(f"  F-mesure : {f_mesure * 100:.2f}\n")

    return metrics_by_product


def analyse_metriques_products_positif(gold_standard, result_file):
    id_products = [
        'AVpf3txeLJeJML43FN82', 'AVphzgbJLJeJML43fA0o', 'AV1YFmcQglJLPUi8IGd1', 'AWIm0C3TYSSHbkXwx3S6',
        'AVpfnp8HLJeJML43AmVi', 'AVpgF1BOilAPnD_xnTsK', 'AVpiUMISilAPnD_xC-hu', 'AVpe8ZRY1cnluZ0-aY4H',
        'AVpfnuDailAPnD_xfKZY', 'AVpgfP3DilAPnD_xtG3M', 'AVpe7vI_ilAPnD_xRMq2', 'AVpgGPyq1cnluZ0-wbTJ',
        'AVphUeKeilAPnD_x3-Be', 'AVqlHaLknnc1JgDc3m5y'
    ]

    metrics_by_product = {product_id: {"VP": 0, "VN": 0, "FP": 0, "FN": 0} for product_id in id_products}
     
    A = 'Positif'
    NA = ['Négatif', 'Neutre']

    with open(gold_standard, mode='r', encoding='utf-8') as gold, open(result_file, mode='r', encoding='utf-8') as res:
        reader1 = csv.DictReader(gold)
        reader2 = csv.DictReader(res)

        for row1, row2 in zip(reader1, reader2):
            product_id = row1['id']
            if product_id in id_products:
                row_gold = row1['reviews.doRecommend']
                row_result = row2['result']

                if row_gold == A and row_result == A:
                    metrics_by_product[product_id]['VP'] += 1
                elif row_gold == A and row_result in NA:
                    metrics_by_product[product_id]['FN'] += 1
                elif row_gold in NA and row_result == A:
                    metrics_by_product[product_id]['FP'] += 1
                elif row_gold in NA and row_result in NA:
                    metrics_by_product[product_id]['VN'] += 1

    # Affichage des métriques pour chaque produit
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
        print(f"  Précision : {precision * 100:.2f}")
        print(f"  Rappel : {rappel * 100:.2f}")
        print(f"  F-mesure : {f_mesure * 100:.2f}\n")

    return metrics_by_product



gold = 'gold_standard.csv'
res = 'results.csv'

analyse_metrique_products(gold, res)
print('\n')
print('-----CLASSE NEGATIVE-----')
analyse_metriques_products_negatif(gold, res)
print('\n')
print('-----CLASSE NEUTRE-----')
analyse_metriques_products_neutre(gold, res)
print('\n')
print('-----CLASSE POSITIVE-----')
analyse_metriques_products_positif(gold, res)

