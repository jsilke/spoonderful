from fastapi import APIRouter, status
from processing.preprocess import prep_data
from data.schemas import Recommendation
import pandas as pd

router = APIRouter(prefix="/recommendations", tags=["Recipes"])


@router.get("/", status_code=status.HTTP_200_OK)
def get_recipes(ingredients: str):
    """
    Query Spoonacular's API for data using the provided ingredient list and apply the recommendation algorithm to return recipe recommendations.
    """
    columns_to_show = ("title", "image", "readyInMinutes", "instructions")
    df = prep_data(ingredients)
    recommendations = _make_recommendations(df, columns_to_show)

    return recommendations


def _make_recommendations(df: pd.DataFrame, columns: tuple) -> dict[Recommendation]:
    """
    Internal function used by `get_recipes` that takes in a DataFrame filtered down to 5 recipes and returns the recommendations in a dictionary.
    """
    recommendations = {
        row.Index: Recommendation(
            name=row.title,
            image=row.image,
            instructions=row.instructions,
            time_minutes=row.readyInMinutes,
        )
        for row in df[columns].itertuples()
    }
    return recommendations
