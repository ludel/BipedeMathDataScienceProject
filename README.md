## Score par produit
Ce script permet de mesurer l'impact d'un produit sur l'avis d'un client.  
Celà ce présente d'un score associé à chaque produit.
La valeur de ce score est comprise entre la note minimale et la note maximale des avis clients.  
Pour calculer le score des produits fournis dans le dataset, exécutez la commande suivante :  
`python3 compute_product_review_score.py --data=/path/to/dataset/directory`  
Ce script créra dans le dossier du dataset un fichier csv apellé `olist_product_scores.csv` qui contiendra les scores associés aux produits.
