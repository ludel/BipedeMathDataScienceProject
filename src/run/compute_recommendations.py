import pandas as pd
from sklearn.cluster import KMeans


class ComputeRecommendation:
    def __init__(self, nb_cluster=60, data_path='../../data'):
        self.df_clustered = None
        self.nb_cluster = nb_cluster
        self.data_path = data_path

    def get_full_merged_df(self):
        df_orders = pd.read_csv(f'{self.data_path}/olist_orders_dataset.csv')
        df_orders_item = pd.read_csv(f'{self.data_path}/olist_order_items_dataset.csv')
        df_product = pd.read_csv(f'{self.data_path}/olist_products_dataset.csv')
        return pd.merge(df_orders, df_orders_item, on='order_id').merge(df_product, on='product_id')

    def create_cluster(self):
        df = self.get_full_merged_df()
        df_cat = df.groupby('customer_id')['product_category_name'].value_counts().unstack(fill_value=0)

        y_pred = KMeans(random_state=5, n_clusters=self.nb_cluster).fit_predict(df_cat)
        cluster_df = pd.DataFrame(data={'customer_id': df_cat.index, 'cluster': y_pred})

        self.df_clustered = pd.merge(df, cluster_df, on='customer_id')

    def import_df(self):
        self.df_clustered = pd.read_csv('../../data/full_clustered.csv')

    def export_df(self):
        self.df_clustered.to_csv('../../data/full_clustered.csv')


if __name__ == '__main__':
    compute = ComputeRecommendation()
    compute.create_cluster()
