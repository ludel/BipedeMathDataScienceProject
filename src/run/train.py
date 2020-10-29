import json
import pickle
import sys
from datetime import datetime
from importlib import import_module

import pandas as pd
from sklearn.pipeline import Pipeline


def main():
    with open(f"../../params/{sys.argv[1]}") as f:
        parameters = json.load(f)

    df_train = pd.read_csv(f"../../{parameters['dataDirectory']}/train.csv")

    label = parameters["label"]
    x_train = df_train[parameters["features"]]
    y_train = df_train[[label]]

    steps = []
    for step in parameters["pipeline"]:
        class_info = step["class"].split(".")
        steps.append(
            (
                step["name"],
                getattr(import_module(".".join(class_info[:-1])), class_info[-1])(*step["args"], **step["kwargs"])
            )
        )

    pipe = Pipeline(steps)

    pipe.fit(x_train, y_train)  # Why fit transforms x_train ?

    file_name = '.'.join(sys.argv[1].split('.')[:-1])
    now = datetime.now()
    with open(f"../../params/ckpts/{file_name}_{now.day}-{now.month}-{now.year}-{now.hour}:{now.minute}", 'wb') as f:
        pickle.dump(pipe, f)


if __name__ == '__main__':
    main()
