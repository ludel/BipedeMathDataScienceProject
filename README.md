## Score par produit
Ce script permet de mesurer l'impact d'un produit sur l'avis d'un client.  
Celà ce présente d'un score associé à chaque produit.
La valeur de ce score est comprise entre la note minimale et la note maximale des avis clients.  
Pour calculer le score des produits fournis dans le dataset, exécutez la commande suivante :  
`python3 compute_product_review_score.py --data=/path/to/dataset/directory`  
Ce script créra dans le dossier du dataset un fichier csv apellé `olist_product_scores.csv` qui contiendra les scores associés aux produits.

## Recommandations par produit et client
Ce script permet de générer des recommandations pour une produit ou un client en particulier. Les deux systèmes utilisent un algorithme qui regroupe les clients similaires afin de leurs proposés des produits en fonction leurs centres d'intérêt.

#### Recommandation client
`python3 compute_recommendations.py --data=/path/to/dataset/directory --client-id=971bf8f42a9f8cb3ead257854905b454`


#### Recommandation produit
`python3 compute_recommendations.py --data=/path/to/dataset/directory --client-id=971bf8f42a9f8cb3ead257854905b454 --product-id=595fac2a385ac33a80bd5114aec74eb8`

#### Arguments optionnels
`--import-clustered-data` permet d'utiliser les clusters générés précédemment.

`--nb-cluster` permet de définir le nombre de cluster (60 par défaut).

`--limit` permet de définir le nombre maximum de recommandations (20 par défaut).
