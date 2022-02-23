import pandas as pd
import numpy as np
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from sklearn.preprocessing import OrdinalEncoder, StandardScaler


def apply_clustering(prepared_data: pd.DataFrame) -> tuple[KMeans, np.ndarray]:
    """
    Apply cluster analysis to the appropriate columns of the prepared DataFrame using a 'force 5' KMeans
    strategy. The `recommended_columns` refers to columns appearing in the recommendations sent to users.
    Returns the fitted clustering (`cluster`) and the transformed data (`X`).
    """
    all_columns = prepared_data.columns.tolist()
    column_indices_dict = _map_columns_to_indices(all_columns)

    pipe = Pipeline(
        [
            (
                "encoding",
                ColumnTransformer(
                    [
                        (
                            "binary_categorical",
                            OrdinalEncoder(),
                            column_indices_dict["binary_features"],
                        ),
                    ],
                    remainder="passthrough",
                ),
            ),
            ("scaling", StandardScaler()),
            ("reduce_dimensions", PCA(n_components=2)),
        ],
    )

    cluster = KMeans(n_clusters=5)

    X = pipe.fit_transform(prepared_data)
    cluster.fit(X)

    return cluster, X


def _map_columns_to_indices(df_columns: list) -> dict[list]:
    """
    Maps the column names to the corresponding numpy array column indices. Note that the current
    iteration of the algorithm does not make use of `continuous_features` but it was used in prior
    versions and may be useful for further transformations.
    """
    column_map = {name: index for index, name in enumerate(df_columns)}

    binary_features = [
        "vegetarian",
        "vegan",
        "glutenFree",
        "dairyFree",
    ]
    continuous_features = list(set(df_columns) - set(binary_features))

    important_classes = {
        "binary_features": [*map(column_map.get, binary_features)],
        "continuous_features": [*map(column_map.get, continuous_features)],
    }

    return important_classes
