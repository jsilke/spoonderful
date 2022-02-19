from fastapi import APIRouter, status
from app.spoonderful.processing.preprocess import prep_recipe_data
from app.spoonderful.processing.pipeline import apply_clustering
from app.spoonderful.data.schemas import Recommendation
from sklearn.pipeline import Pipeline
from sklearn.metrics import pairwise_distances_argmin_min
import pandas as pd
import numpy as np

router = APIRouter(prefix="/recommendations", tags=["Recipes"])


@router.get("/simple", status_code=status.HTTP_200_OK)
def get_similar_recipies(ingredients: str):
    """
    Query Spoonacular's API for data using the provided ingredient list and return the top 5 (or fewer) recipe recommendations.
    """
    columns_to_show = ["id", "title", "image", "readyInMinutes", "instructions"]
    df = prep_recipe_data(ingredients)
    recommendations = _make_recommendations(df, columns_to_show)

    return recommendations


@router.get("/varied", status_code=status.HTTP_200_OK)
def get_varied_recipes(ingredients: str):
    """
    Query Spoonacular's API for data using the provided ingredient list and apply unsupervised learning to return diverse recipe recommendations.
    """
    columns_to_show = ["id", "title", "image", "readyInMinutes", "instructions"]
    df = prep_recipe_data(ingredients, 100)

    if df.shape[0] > 5:
        clustering, X = apply_clustering(df.drop(columns=columns_to_show))
        indices = _get_recommendation_indices_from_clusters(clustering, X)
        df = df.iloc[indices]

    recommendations = _make_recommendations(df, columns_to_show)

    return recommendations


def _get_recommendation_indices_from_clusters(
    clustering: Pipeline, data: pd.DataFrame
) -> np.ndarray:
    """
    Retrieves the 5 recipes from the cluster analysis that are closest to the centroids of each
    cluster in the fitted pipeline.
    `pipe` = The fitted pipeline.
    `data` = The transformed data.
    """
    closest, _ = pairwise_distances_argmin_min(clustering.cluster_centers_, data)
    return closest


def _make_recommendations(df: pd.DataFrame, columns: tuple) -> dict[Recommendation]:
    """
    Internal function used by `get_recipes` that takes in a DataFrame filtered down to 5 recipes and returns the recommendations in a dictionary.
    """
    recommendations = {
        row.id: Recommendation(
            name=row.title,
            image=row.image,
            instructions=row.instructions,
            time_minutes=row.readyInMinutes,
        )
        for row in df[columns].itertuples()
    }
    return recommendations
