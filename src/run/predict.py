import json
import pickle
import sys

import pandas as pd


def main():
    with open(f"../../params/ckpts/{sys.argv[2]}", 'rb') as f:
        pipe = pickle.load(f)

    with open(f"../../params/{sys.argv[1]}") as f:
        parameters = json.load(f)

    df_test = pd.read_csv(f"../../{parameters['data_directory']}/test.csv")
    x_test = df_test[parameters['features']]

    y_test_pred = pipe.predict(x_test)

    pd.DataFrame(
        {
            "PassengerId": df_test["PassengerId"],
            "Survived": y_test_pred,
        }
    ).to_csv("../../data/titanic/prediction.csv", index=False)


if __name__ == '__main__':
    main()
