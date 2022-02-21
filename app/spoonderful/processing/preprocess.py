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
    recipe_quantity: int,
    response: SpoonacularResponse,
    strategy: DataRetrievalStrategy,
) -> list[dict, str, object]:
    """
    Uses the SpoonacularResponse.classmethod to query a Spoonacular endpoint and retrieve
    the data defined in the strategy class. Returns response JSON data.
    """
    spoon = response(query, recipe_quantity)
    retrieval_strategy = strategy()

    return spoon.get_data(retrieval_strategy)


def prep_recipe_data(
    query: str,
    recipe_quantity: int = 5,
    response: SpoonacularResponse = SpoonacularResponse.get_recipes,
    strategy: DataRetrievalStrategy = ComplexRetrievalStrategy,
):
    """
    Get the Spoonacular response and preprocess the recipe JSON data in preparation for recommendation.
    """
    # TODO increase cohesion here.

    data = retrieve_data(query, recipe_quantity, response, strategy)

    df = pd.DataFrame(data)
    try:
        df = df.drop(columns=["nutrition", "analyzedInstructions"])
    except KeyError:
        print("No results retrieved for provided ingredients.")
        return df

    nutrition_data = []
    instruction_data = []
    for recipe in data:
        nutrition_data.append(recipe.get("nutrition"))
        instruction_data.append(recipe.get("analyzedInstructions"))

    calories = tab.CaloricBreakdownTabulator()
    calorie_df = calories.tabulate_data(nutrition_data)

    nutrients = tab.NutrientDailyNeedsTabulator()
    nutrient_df = nutrients.tabulate_data(nutrition_data)

    instructions = tab.InstructionsTabulator()
    instructions_df = instructions.tabulate_data(instruction_data)

    frames = [df, calorie_df, nutrient_df, instructions_df]
    aggregate_df = pd.concat(frames, axis=1)
    aggregate_df = aggregate_df.fillna(0)

    return aggregate_df
