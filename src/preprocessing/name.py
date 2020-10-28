from sklearn.base import BaseEstimator, TransformerMixin


def extract_title(name):
    title = name.split('.')[0].split(', ')[1].lower()
    titles = {'mr', 'miss', 'mrs', 'master', 'dr', 'rev'}
    return title if title in titles else 'default'


class NameExtractor(BaseEstimator, TransformerMixin):
    def fit(self, x, y=None):
        return self

    def transform(self, x, y=None):
        x['Name'] = x['Name'].map(extract_title)
        return x
