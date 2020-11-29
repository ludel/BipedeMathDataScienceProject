import argparse
from collections import Counter

import pandas as pd
from sklearn.cluster import KMeans


class ComputeRecommendation:
    def __init__(self, nb_cluster: int, data_path: str, limit: int):
        self.df_clustered = None
        self.nb_cluster = nb_cluster
        self.data_path = data_path
        self.limit = limit

        df_orders = pd.read_csv(f'{self.data_path}/olist_orders_dataset.csv')
        df_orders_item = pd.read_csv(f'{self.data_path}/olist_order_items_dataset.csv')
        df_product = pd.read_csv(f'{self.data_path}/olist_products_dataset.csv')
        self.df = pd.merge(df_orders, df_orders_item, on='order_id').merge(df_product, on='product_id')

    def create_cluster(self):
        df_cat = self.df.groupby('customer_id')['product_category_name'].value_counts().unstack(fill_value=0)

        y_pred = KMeans(random_state=5, n_clusters=self.nb_cluster).fit_predict(df_cat)
        cluster_df = pd.DataFrame(data={'customer_id': df_cat.index, 'cluster': y_pred})

        self.df_clustered = pd.merge(self.df, cluster_df, on='customer_id')
        self.export_df()

    def get_cluster_group(self, current_user: str) -> pd.DataFrame:
        assert self.df_clustered is not None, 'Clustered dataframe is not generated.'

        customer = self.df_clustered.loc[self.df_clustered['customer_id'] == current_user]
        return self.df_clustered.loc[self.df_clustered['cluster'] == customer['cluster'].iloc[0]]

    def predict_for_product(self, current_user: str, current_product: str) -> list:
        cluster_group = self.get_cluster_group(current_user)

        orders_with_same_product = cluster_group.loc[cluster_group['product_id'] == current_product, 'order_id']
        recommended_products = []
        for order_id in orders_with_same_product:
            order = self.df_clustered.loc[self.df_clustered['order_id'] == order_id]
            for product in order.loc[order['product_id'] != current_product, 'product_id']:
                recommended_products.append(product)

        return sorted(Counter(recommended_products))[:self.limit]

    def predict_for_client(self, current_user: str) -> list:
        cluster_group = self.get_cluster_group(current_user)
        return sorted(Counter(cluster_group['product_id']))[:self.limit]

    def import_df(self):
        self.df_clustered = pd.read_csv(f'{self.data_path}/full_clustered.csv')

    def export_df(self):
        print('Export clustered data ...')
        self.df_clustered.to_csv(f'{self.data_path}/full_clustered.csv')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--data', help='Path to data directory', required=True)
    parser.add_argument('--nb-cluster', help='Number of cluster (default:60)', default=60)
    parser.add_argument('--limit', help='Limit of product (default:20)', default=20)
    parser.add_argument('--import-clustered-data', help='Use clustered dataframe previously generated',
                        action="store_true")
    parser.add_argument('--client-id', required=True)
    parser.add_argument('--product-id', required=False)
    args = parser.parse_args()

    compute = ComputeRecommendation(args.nb_cluster, args.data, args.limit)
    print('Loading data ...')
    if args.import_clustered_data:
        compute.import_df()
    else:
        compute.create_cluster()

    if args.product_id:
        print('Recommendation for a specific product')
        recommendation = compute.predict_for_product(args.client_id, args.product_id)
    else:
        print('Recommendation for a client')
        recommendation = compute.predict_for_client(args.client_id)

    print('Products recommendation :', ', '.join(recommendation))
