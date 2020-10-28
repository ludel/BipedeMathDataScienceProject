from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from src.preprocessing.name import NameExtractor

pipe = Pipeline(
  [
    ('scaler', StandardScaler()),
    ('regression', LogisticRegression()),
    ('name', NameExtractor())
  ]
)
