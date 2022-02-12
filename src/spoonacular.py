import requests as rq
import os

# I could also use protocols, the __call__ method, or functions here too, but I think this annotation is less ambiguous than the alternatives.
from abc import ABC, abstractmethod


class DataRetrievalStrategy(ABC):
    """
    Abstract base class for different data retrieval strategies.
    """

    @abstractmethod
    def retrieve_data(self, json_data: list[dict]) -> list[dict]:
        """
        The abstract method that will implement the data retrieval strategy.
        """
        pass


class RecipeRetrievalStrategy(DataRetrievalStrategy):
    """
    Retrieving meal data from the SpoonacularResponse.
    """

    def retrieve_data(self, json_data: list[dict]) -> list[dict]:
        """
        A concrete data retrieval strategy to extract recipe fields from the response json.
        """
        recipe_data = [
            {
                "id": recipe["id"],
                "title": recipe.get("title"),
                "used_ingredient_count": recipe.get("usedIngredientCount"),
                "missed_ingredient_count": recipe.get(
                    "missedIngredientCount"
                ),  # can add the specific ingredients later.
                "likes": recipe.get("likes"),
            }
            for recipe in json_data
        ]

        return recipe_data


class SpoonacularResponse:
    """
    Class to make requests to Spoonacular's API and store the response data.
    """

    API_KEY = os.getenv("spoonacular")
    # RapidAPI's Spoonacular entry point.
    ENTRY_POINT = "https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com/"
    HEADERS = {
        "x-rapidapi-host": "spoonacular-recipe-food-nutrition-v1.p.rapidapi.com",
        "x-rapidapi-key": API_KEY,
    }

    # Ideally just use the classmethods to instantiate based on the desired endpoint.
    def __init__(self, response: rq.Response = None, data: dict = None):
        self.response = response
        self.data = data

    @classmethod
    def get_recipes_from_ingredients(cls, ingredients: str) -> dict:
        """
        Retrieve recipies from Spoonacular's API using a list of ingredients formatted as a comma-seperated string.
        See https://spoonacular.com/food-api/docs#Search-Recipes-by-Ingredients.
        """
        ENDPOINT = "recipes/findByIngredients"
        URL = f"{cls.ENTRY_POINT}{ENDPOINT}"
        PARAMETERS = {
            "ingredients": ingredients,
            "ranking": 2,  # minimize missing ingredients as a priority.
            "ignorePantry": True,  # Assume that all available ingredients are in the list.
        }

        response = rq.get(URL, params=PARAMETERS, headers=cls.HEADERS)
        status = cls.check_response_status(response)
        print(status[1])
        if status[0]:
            return cls(response, response.json())
        else:
            return cls(response)

    @staticmethod
    def check_response_status(response: rq.Response) -> tuple[int, str]:
        """
        Reports on the response status code and how many daily requests are remaining.
        """
        MDN_STATUS = "https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/"
        status_code = response.status_code
        info = f"{MDN_STATUS}{status_code}"
        # I was advised to monitor these headers by the Spoonacular team to help avoid additional charges.
        _ratelimit_headers = [
            "X-Ratelimit-Classifications-Limit",
            "X-Ratelimit-Classifications-Remaining",
            "X-Ratelimit-Requests-Limit",
            "X-Ratelimit-Requests-Remaining",
            "X-Ratelimit-Tinyrequests-Limit",
            "X-Ratelimit-Tinyrequests-Remaining",
        ]

        for header in _ratelimit_headers:
            print(f"{header}: {response.headers.get(header)}")

        return (status_code == 200), info

    def get_data(self, retrieval_strategy: DataRetrievalStrategy) -> dict:
        """
        Returns response data based on a concrete retrieval_strategy object that inherits from the DataRetrievalStrategy abstract base class.
        """
        retrieved_data = retrieval_strategy.retrieve_data(self.data)

        return retrieved_data


def main():
    pass


if __name__ == "__main__":
    main()
