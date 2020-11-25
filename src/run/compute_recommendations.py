import pandas as pd
from sklearn.cluster import KMeans


class ComputeRecommendation:
    def __init__(self):
        self.df_orders = pd.read_csv("../data/olist_orders_dataset.csv")
        self.df_orders_item = pd.read_csv("../data/olist_order_items_dataset.csv")
        self.df_product = pd.read_csv("../data/olist_products_dataset.csv")
        self.df_clustered = None

    def create_cluster(self):
        df = pd.merge(self.df_orders, self.df_orders_item, on='order_id')
        df = pd.merge(df, self.df_product, on='product_id')

        df_cat = df.groupby('customer_id')['product_category_name'].value_counts().unstack(fill_value=0)

        y_pred = KMeans(random_state=5, n_clusters=60).fit_predict(df_cat)
        cluster_df = pd.DataFrame(data={'customer_id': df_cat.index, 'cluster': y_pred})

        self.df_clustered = pd.merge(df, cluster_df, on='customer_id')

    def import_df(self):
        self.df_clustered = pd.read_csv('../data/full_clustered.csv')

    def export_df(self):
        self.df_clustered.to_csv('../data/full_clustered.csv')
