# allocine-classification

**Groupe :** G08_NAVARRO-VERY_GRIETTE

**Membres :**
- Anthony NAVARRO
- Milan VERY-GRIETTE

Ce dépôt contient les sources du projet "Défi 2" du module d'application d'innovation (année 2023-2024).


## CORPUS

Les deux projets de ce dossier contiennent le code ayant permis de réaliser les statistiques et graphiques de l'analyse de corpus du projet.

## JavaScript

Le projet NodeJS original, permettant de réaliser l'analyse. Suite à une limitation de Javascript ne permettant pas d'ouvrir le fichier de données de train, celui-ci a été intégralement recodé en Python.

## Python

La version du projet d'analyse de corpus recodé en Python.


## SVM

Projet permettant de générer un index, ainsi que des fichiers au format `.svm`, compatibles avec LibSVM.


## LSTM

### lstm-main.py

Code d'entrainement Keras d'un modèle LSTM, avec sauvegarde de celui-ci.

### lstm-run.py

Code chargeant un modèle LSTM et effectuant une prédiction.


## BERT

### bert-base.py

Code d'entraînement Keras d'un modèle transformers basé sur [camembert-base](https://huggingface.co/camembert-base).

### bert-allocine.py

Code d'entraînement Keras d'un modèle transformers basé sur [tblard/tf-allocine](https://huggingface.co/tblard/tf-allocine).


## DATA AUGMENTATION

### duplicate.py

Code permettant de dupliquer des commentaires dans le corpus.

### remove_duplicates.py

Sert à retirer des doublons parmi les commentaires du corpus (permet de garantir l'unicité des commentaires).

### augment_synonym.py

Applique une augmentation des données basée sur des substitutions avec des synonymes dans le corpus.

### SCRAPING

Utilitaire de web scraping permettant de récupérer de véritables commentaires directement depuis AlloCiné.
