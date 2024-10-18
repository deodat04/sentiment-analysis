# Analyse de sentiments
# Execution du programme | Approche naive


## 1. Ouvrir  le terminal 
`ctrl+alt+t`

## 2. Se connecter à l'environnement virtuel tp_python
`source /usr/bin/tp_python_virtualenv`

## 3. Naviguer vers le répertoires du projet
`cd repertoire/du/projet`

## 4. Executer le programme
`python naive_feeling.py`

## 5. Informations nécessaire suite à l'execution du programme
- après exécution du programme suivez les instructions si
vous souhaitez visualiser les synonymes générés par Wordnet 
pour l'analyse de corpus
- (taper **1** pour accéder à la liste des synonymes et **2** pour ne pas y accéder)
- En ouvrant le répertoire du projet, un ficher **results.csv**
est généré et affiche les résultats de chaque avis.

## 6. Désactiver l'environnement virtuel
`deactivate`

## 7. Lien vers dépôt github du projet
[Sentiment-Analysis sur GitHub](https://github.com/deodat04/sentiment-analysis.git)


## 8. Informations sur certains fichiers et dossier du projet
- metriques.py est le programme permettant de calculer l'exactitude de cette approche
- assets contient les images utilisées dans le rapport qui présentent les différentes approches
- ElectronicsReviews.csv représente le corpus initial et gold_standard.csv le gold standard


- https://github.com/nltk/nltk/blob/develop/nltk/sentiment/vader.py
- https://stackoverflow.com/questions/40325980/how-is-the-vader-compound-polarity-score-calculated-in-python-nltk