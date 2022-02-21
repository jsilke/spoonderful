from fastapi import APIRouter, status, HTTPException
from app.spoonderful.processing.preprocess import prep_recipe_data
from app.spoonderful.processing.pipeline import apply_clustering
from app.spoonderful.data.schemas import Recommendation
from sklearn.pipeline import Pipeline
from sklearn.metrics import pairwise_distances_argmin_min
import pandas as pd
import numpy as np

router = APIRouter(prefix="/recommendations", tags=["Recipes"])
# These columns will be excluded from analysis and shown to the user. Note that a change here requires a change to the Recommendation schema.
COLUMNS_TO_SHOW = ["id", "title", "image", "readyInMinutes", "instructions"]


@router.get("/simple", status_code=status.HTTP_200_OK)
def get_similar_recipies(ingredients: str):
    """
    Query Spoonacular's API for data using the provided ingredient list and return the top 5 (or fewer) recipe recommendations.
    """
    df = prep_recipe_data(ingredients)
    try:
        recommendations = _make_recommendations(df)
    except KeyError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Oh no! It looks like Spoonacular doesn't have recipes with only: {ingredients}! Try double checking your spelling and/or adding more ingredients!",
        )

    return recommendations


@router.get("/varied", status_code=status.HTTP_200_OK)
def get_varied_recipes(ingredients: str):
    """
    Query Spoonacular's API for data using the provided ingredient list and apply unsupervised learning to return diverse recipe recommendations.
    """
    df = prep_recipe_data(ingredients, 100)

    if df.shape[0] > 5:
        clustering, principal_component_coordinates = apply_clustering(
            df.drop(columns=COLUMNS_TO_SHOW)
        )
        indices = _get_recommendation_indices_from_clusters(
            clustering, principal_component_coordinates
        )
        df = df.iloc[indices]

    try:
        recommendations = _make_recommendations(df)
    except KeyError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Oh no! It looks like Spoonacular doesn't have recipes with only: {ingredients}! Try double checking your spelling and/or adding more ingredients!",
        )

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


def _make_recommendations(df: pd.DataFrame) -> dict[Recommendation]:
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
        for row in df[COLUMNS_TO_SHOW].itertuples()
    }
    return recommendations
