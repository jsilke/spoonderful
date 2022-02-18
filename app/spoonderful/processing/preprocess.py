from app.spoonacular.response import SpoonacularResponse
from app.spoonacular.retrieval import ComplexRetrievalStrategy, DataRetrievalStrategy
from . import tabulation as tab
import pandas as pd


def get_query(path: str = "../data/my_food.txt") -> str:
    """
    Used to get a comma-separated string of ingredients from a file to use as a query
    for Spoonacular's API (assuming defaults in this script are used). The type of data
    used here can vary depending on which Spoonacular endpoint the user wishes to query.
    """
    with open(path, "r") as file:
        query = file.read()

    return query


def retrieve_data(
    query: str,
    response: SpoonacularResponse = SpoonacularResponse.get_recipes,
    strategy: DataRetrievalStrategy = ComplexRetrievalStrategy,
) -> list[dict, str, object]:
    """
    Uses the SpoonacularResponse.classmethod to query a Spoonacular endpoint and retrieve
    the data defined in the strategy class. Returns response JSON data.
    """
    spoon = SpoonacularResponse.get_recipes(query)
    retrieval_strategy = ComplexRetrievalStrategy()

    return spoon.get_data(retrieval_strategy)


def prep_data(query: str):
    """
    Get and preprocess Spoonacular response data in preparation for recommendation.
    """
    # TODO Refactor to generalize better.

    data = retrieve_data(query)

    df = pd.DataFrame(data)
    df = df.drop(columns=["nutrition", "analyzedInstructions"])

    nutrition_data = []
    instruction_data = []
    for recipe in data:
        nutrition_data.append(recipe["nutrition"])
        instruction_data.append(recipe["analyzedInstructions"])

    calories = tab.CaloricBreakdownTabulator()
    calorie_df = calories.tabulate_data(nutrition_data)

    nutrients = tab.NutrientDailyNeedsTabulator()
    nutrient_df = nutrients.tabulate_data(nutrition_data)

    instructions = tab.InstructionsTabulator()
    instructions_df = instructions.tabulate_data(instruction_data)

    frames = [df, calorie_df, nutrient_df, instructions_df]
    aggregate_df = pd.concat(frames, axis=1)

    aggregate_df = aggregate_df.fillna(0)
    aggregate_df = aggregate_df.set_index("id")

    return aggregate_df
