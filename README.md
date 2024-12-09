# Projet_kit_big_data

Lien vers la Webapp Déployée :
https://projetkitbigdata-ipja7lrnugkzoh5way2ngf.streamlit.app

##### Par Damien Thai, Baptiste Cervoni, Alexandre Malfoy, Alexandre Rocchi

Notre axe pour ce projet *Kit Big Data* à été de présenter une analyse approfondie des données du site [Food.com](https://www.food.com/) (données issues d’un dataset disponible sur [Kaggle](https://www.kaggle.com/datasets/shuyangli94/food-com-recipes-and-user-interactions)) afin d’expliquer la baisse d’activité observée ces dernières années. Il s’agit d’un travail dans lequel nous jouons le rôle d’une équipe de data analystes conseillant les propriétaires du site sur les raisons de cette perte de popularité et proposant des axes d’amélioration.

---

## Contexte et Objectifs

**Contexte :**  
Food.com était une référence en matière de partage et de recommandations de recettes. Cependant, depuis 2010, la diminution du trafic et de l’engagement des utilisateurs sur le site a pu être constatés. L’objectif de cette étude, est d'analyser les recettes les plus populaires afin de redynamiser le site en promouvant ou proposant des recettes similaires.

**Objectifs du Projet :**
1. Pretraiter la base de données afin de supprimer les outliers, d'obtenir des informations supplémentaires (note moyenne, nombre de commentaires, ...)
2. Analyser les tendances du site au fil du temps pour identifier les périodes de croissance et de déclin.
3. Analyser les critères selon lesquelles une recette peut être qualifié de populaire, telles que la note moyenne et le nombre de commentaires.
4. Comprendre les facteurs de succès des recettes populaires : durée, nombre d'étapes, ingrédients, ...
5. Proposer un clustering thématique des recettes afin de faire resortir les catégories de recettes populaires
6. Présenter l’analyse via une webapp Streamlit interactive permettant une exploration intuitive des résultats par les décideurs.

---

## Organisation du Code

L’architecture du projet est structurée pour favoriser la modularité et la maintenabilité :

```bash
PROJET_KIT_BI/
├─ data/       
│  └─ ...                    # Données brutes (CSV)
├─ data_processing/          # scripts de préparation et nettoyage des données
├─ scripts/
│  └─ pipeline_preprocess.py # pipeline du préprocessing, à lancer avec les données brutes
├─ src/
│  ├─ documentation/         # documentation Sphinx
│  └─ pages/                 # scripts Python pour les pages streamlit
│     ├─ Analyse_des_donnees.py
│     ├─ Clustering.py
│     ├─ DataViz.py
│     ├─ Preprocessing.py
│     └─ Simulation_Carte.py
├─ utils/
│  ├─ base_study.py          # Classe danalyse mère
│  ├─ bivariate_study.py     # Classe dAnalyses bivariées
│  ├─ load_functions.py      # Chargement des données
│  ├─ score_functions.py     # fonction de calcul de scores et métriques
│  ├─ univariate_study.py    # Classe danalyses univariées
│  └─ logging_config.py      # Configuration des logs
├─ tests/                    # Tests unitaires avec pytest
│  ├─ test_base_study.py
│  ├─ test_data_load.py
│  └─ ...
├─ .gitignore
├─ main.py                

```
---

## Installation et Exécution

1. **Cloner le Projet :**
  ```bash
   git clone https://github.com/votrecompte/nomduprojet.git
   cd nomduprojet
  ```
2. Installation des dépendences (Python 3.12.3) :

  ```bash
   pip install -r requirements.txt
  ```
3. Démarrer la Webapp :
  ```bash
   python3 run main.py
  ```
  Ouvrez le lien local fourni dans votre navigateur. Vous découvrirez une interface présentant différentes analyses, visualisations et outils d’exploration.

## Tests et Qualité

1. Tests Unitaires :
  ```bash
    pytest --cov=src
  ```
La couverture des tests est de 77 %. Ce score s'explique par la difficulité de tester l'affichage de tous les graphes de la page d'analyse de données


2. Qualité du Code : 

Le code suit les normes PEP 8, utilise le type hinting et des docstrings. Un pipeline CI/CD via GitHub Actions valide le respect des normes, des tests et du coverage.

## Documentation

La documentation technique (classes, fonctions, modules) est générée par Sphinx.
  Vous pouvez la consulter directement dans src/documentation/build/html/index.html.
  Pour la régénérer :

  ```bash
    cd src/documentation
    ./make.bat html
```

## Déploiement et CI/CD

Un pipeline GitHub Actions est configuré pour :
  1. Vérifier le linting et le style (PEP 8)
  2. Lancer les tests unitaires et vérifier la couverture
  3. Assurer la présence de docstrings
  
## Pistes d’Amélioration

Améliorations possibles :
  1. Stockage et requêtes via une base de données plus performante pour améliorer. Une version ulltérieur de l'application a   utilisé une base de données MongoDB hébergé sur le cloud via Atlas. Cependant, nous avons été confronté à la limite du le flux d'échange entre l'utilisateur et la base de données. Cette piste à donc été abandonnée pour la version finale mais le code peut être consulté dans la branche dev_mongoDB.
  2. Ajout de fonctionnalités comme la génération automatique de noms de recettes à partir du profil des recettes populaires déterminé dans l'étude.
  3. Profiling des créateurs de recette car ceux sont eux qui sont les premiers moteurs d'activités et Analyse du cycle de vie des recettes.


