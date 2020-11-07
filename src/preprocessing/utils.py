from typing import List

import numpy as np
import scipy.stats
import pandas as pd


def remove_outliers(df: pd.DataFrame, columns: List[str], times=1):
    inner_df = df[columns]
    for _ in range(times):
        inner_df = inner_df[(np.abs(scipy.stats.zscore(inner_df)) < 3).all(axis=1)]
    for column in columns:
        df[column] = inner_df[column]
    return df
