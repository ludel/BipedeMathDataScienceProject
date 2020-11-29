import os
import sys
from typing import Dict, Union, List

import numpy as np
import pandas as pd

# Import data
print('loading data ...')
DATA_DIR_PATH = sys.argv[1].split("--data=")[1]
df_reviews = pd.read_csv(os.path.join(DATA_DIR_PATH, "olist_order_reviews_dataset.csv"))
df_orders = pd.read_csv(os.path.join(DATA_DIR_PATH, "olist_orders_dataset.csv"))
df_order_items = pd.read_csv(os.path.join(DATA_DIR_PATH, "olist_order_items_dataset.csv"))


# Merge dataframes to build the one which interest us
df_orders_reviews = pd.merge(df_orders, df_reviews, on="order_id")
df_orders_reviews_order_items = pd.merge(df_orders_reviews, df_order_items, on="order_id")
# Keep olnly the columns we will use
df = df_orders_reviews_order_items[["order_id", "review_id", "review_score", "product_id"]]


# Group by order
grouped_by_order = df.groupby(["order_id", "review_id", "review_score"])


# Iter the df a first time to pre compute all what we need
print('pre-computing ... (may take up to 30s depending on your hardware')
score_by_product_id: Dict[str, Dict[str, Union[float, List[float]]]] = {}
for (order_id, review_id, review_score), order_rows in grouped_by_order:
    for product_id in {row[3] for row in order_rows.values}:
        if product_id not in score_by_product_id:
            score_by_product_id[product_id] = {"coef": 0, "score": 0}
        coef = np.count_nonzero(order_rows.values[:, 3] == product_id) / order_rows.shape[0]
        score_by_product_id[product_id]["coef"] += coef
        score_by_product_id[product_id]["score"] += coef * review_score


# Compute the products scores using the precomputed data
# And store it into lists to later build a data frame
print('computing scores by product ...')
product_ids = []
product_scores = []
for product_id, score_data in score_by_product_id.items():
    score = score_data["score"] / score_data["coef"]
    score_by_product_id[product_id]["score_final"] = score
    product_ids.append(product_id)
    product_scores.append(score)


# Build a data frame with the products scores and store it into a csv file
print('writing to csv ...')
scores = pd.DataFrame({"product_id": product_ids, "score": product_scores})
scores.to_csv(os.path.join(DATA_DIR_PATH, "olist_product_scores.csv"), index=False)

print('done')
