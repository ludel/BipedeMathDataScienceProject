# %%

import pandas as pd
import seaborn as sns
import numpy as np
from src.preprocessing.utils import remove_outliers

# %%

df_reviews = pd.read_csv("data/olist_order_reviews_dataset.csv")
df_orders = pd.read_csv("data/olist_orders_dataset.csv")
df_order_items = pd.read_csv("data/olist_order_items_dataset.csv")

# %%

df_orders_reviews = pd.merge(df_orders, df_reviews, on='order_id')
df_orders_reviews_order_items = pd.merge(
    df_orders_reviews,
    df_order_items, on='order_id',
)

# %%

df = df_orders_reviews_order_items[['review_id', 'product_id', 'review_score']]

# %%

score_by_product_id = {}
for (review_id, review_score), review_rows in df.groupby(['review_id', 'review_score']):
    product_ids = {product_id for product_id, _, _ in review_rows.values}
    nbr_of_different_products = len(product_ids)
    if nbr_of_different_products > 1:
        for product_id in product_ids:
            if product_id not in score_by_product_id:
                score_by_product_id[product_id] = {'coef': 0, 'scores': []}
            coef = 1 / nbr_of_different_products
            score_by_product_id[product_id]['coef'] += coef
            score_by_product_id[product_id]['scores'].append(review_score * coef / nbr_of_different_products)
    else:
        raise RuntimeError('review without product')

# %%
for product_id, score_data in score_by_product_id.items():
    score_by_product_id[product_id]['score'] = sum(score_data['scores']) / score_data['coef']
