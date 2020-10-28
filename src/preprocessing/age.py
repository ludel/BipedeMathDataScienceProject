from sklearn.base import BaseEstimator, TransformerMixin


class AgeTransformer(BaseEstimator, TransformerMixin):
    def fit(self, x, y=None):
        return self

    def transform(self, x, y=None):
        x['Age'] = x['Age'].fillna(x['Age'].mean())
        return x
