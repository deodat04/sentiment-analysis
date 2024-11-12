# Analyse de sentiments
# Execution du programme


## 1. Ouvrir  le terminal 
`ctrl+alt+t`

## 2. Se connecter à l'environnement virtuel tp_python
`source /usr/bin/tp_python_virtualenv`

## 3. Naviguer vers le répertoires du projet
`cd repertoire/du/projet`

## 4. Executer le programme d'approche naïve
`python naive_feeling.py`

## 4-1. Informations nécessaire suite à l'execution du programme d'approche naïve
- après exécution du programme suivez les instructions si
vous souhaitez visualiser les synonymes générés par Wordnet 
pour l'analyse de corpus
- (taper **1** pour accéder à la liste des synonymes et **2** pour ne pas y accéder)
- En ouvrant le répertoire du projet, un ficher **results.csv**
est généré et affiche les résultats de chaque avis.

## 5. Executer le programme d'approche intelligente
`python intelligent_feeling.py`

## 5.1  Informations nécessaire suite à l'execution du programme d'approche intelligente

### 5.1.1 Métriques
- le programme calcul la précison, le rappel et la f-mesure par classe de sentiments
- le programme calcul l'exactitude générale de cette approche
- la précision, le rappel et la f-mesure sont calculés pour chacune des 14 catégories de produits du corpus

### 5.1.2 Histogrammes
- le programme génère un histogramme permettant de visualiser l'analyse des sentiments de tous les avis du corpus : **hist_sentiments.png**
- un histogramme permettant de visualiser les proportions des avis par classe de sentiment : **proportion_sentiments.png**
- 14 histogrammes permettant de visualiser la proportion des sentiments pour chaque catégorie de produit : **sentiments_produit_{product_id}.png**

## 6. Désactiver l'environnement virtuel
`deactivate`

## 7. Lien vers dépôt github du projet
[Sentiment-Analysis sur GitHub](https://github.com/deodat04/sentiment-analysis.git)


## 8. Informations sur certains fichiers et dossier du projet
- **metriques.py** est le programme permettant de calculer l'exactitude et la précision de l'approche naïve. Il faut avoir exécuter au préalable le fichier **naive_feeling.py** car les métriques sont calculées grâce au fichier **results.csv**. 
- **assets** contient les images utilisées dans le rapport.
- **ElectronicsReviews.csv** représente le corpus initial et **gold_standard.csv** le gold standard.
- **metriques_products.py** permet de calcul les métriques des différentes classes pour chaque catégorie de produit.
- **synonyms.py** permet de générer les synonymes via Wordnet. Il faut renseigner dans le fichier les mots pour lesquels vous souhaitez rechercher les synonymes.


## 9. Execution des programmes python mentionnés à l'étape 8
- `python nom_du_fichier.py`