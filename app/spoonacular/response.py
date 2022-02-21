from __future__ import annotations
import requests as rq
import os
from .retrieval import DataRetrievalStrategy  # . needed because modules not packaged
from typing import Optional
from app.spoonderful.config import settings


class SpoonacularResponse:
    """
    Class to make requests to Spoonacular's API and store the response data.
    """

    RAPID_API_KEY = settings.spoonacular_key
    # RapidAPI's Spoonacular entry point.
    ENTRY_POINT = "https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com/"
    HEADERS = {
        "x-rapidapi-host": "spoonacular-recipe-food-nutrition-v1.p.rapidapi.com",
        "x-rapidapi-key": RAPID_API_KEY,
    }

    # Use the classmethods to instantiate based on the desired endpoint.
    def __init__(self, response: rq.Response = None, data: dict = None):
        self.response = response
        self.data = data

    @staticmethod
    def _check_response(response: rq.Response) -> rq.Response.status_code:
        """
        Reports on the response status code and how many daily requests are remaining.
        Used internally by `_make_request_and_check_response`.
        """
        MDN_HTTP_STATUS = "https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/"
        status_code = response.status_code
        info = f"{MDN_HTTP_STATUS}{status_code}"
        print(info)

        _ratelimit_headers = [
            "X-Ratelimit-Classifications-Limit",
            "X-Ratelimit-Classifications-Remaining",
            "X-Ratelimit-Requests-Limit",
            "X-Ratelimit-Requests-Remaining",
            "X-Ratelimit-Tinyrequests-Limit",
            "X-Ratelimit-Tinyrequests-Remaining",
        ]
        for header in _ratelimit_headers:
            value = response.headers.get(header)
            if value:
                print(f"{header}: {value}")

        return status_code

    @classmethod
    def _make_request_and_check_response(
        cls, url: str, parameters: str, headers: Optional[str] = None
    ) -> SpoonacularResponse:
        """
        Used internally by classmethods to complete and check requests.
        """
        response = rq.get(
            url,
            params=parameters,
            headers=headers,
        )

        if cls._check_response(response):
            return cls(response, response.json())

        return cls(response)

    @classmethod
    def get_recipes_from_ingredients(cls, ingredients: str) -> SpoonacularResponse:
        """
        Get recipies from Spoonacular's API using a list of ingredients formatted as a comma-seperated string.
        See: https://spoonacular.com/food-api/docs#Search-Recipes-by-Ingredients
        """
        ENDPOINT = "recipes/findByIngredients"
        URL = f"{cls.ENTRY_POINT}{ENDPOINT}"
        parameters = {
            "ingredients": ingredients,
            "ranking": 2,  # minimize missing ingredients as a priority.
            "ignorePantry": True,  # Assume that all available ingredients are in the list.
        }

        spoonacular_response = cls._make_request_and_check_response(
            url=URL,
            parameters=parameters,
            headers=cls.HEADERS,
        )

        return spoonacular_response

    @classmethod
    def get_taste_from_recipe_id(cls, recipe_id: int) -> SpoonacularResponse:
        """
        Get a taste vector associated with a recipe id.
        See: https://spoonacular.com/food-api/docs#Taste-by-ID
        """
        ENDPOINT = f"recipes/{recipe_id}/tasteWidget.json"
        # This functionality does not appear to exist on RapidAPI.
        SPOONACULAR_KEY = os.getenv("spoon_key")
        URL = f"https://api.spoonacular.com/{ENDPOINT}"
        parameters = {
            "apiKey": SPOONACULAR_KEY,
            "id": recipe_id,
        }

        spoonacular_response = cls._make_request_and_check_response(
            url=URL,
            parameters=parameters,
        )

        return spoonacular_response

    @classmethod
    def get_recipes(cls, ingredients: str, number: int) -> SpoonacularResponse:
        """
        Query recipes using Spoonacular's complex search.
        See: https://spoonacular.com/food-api/docs#Search-Recipes-Complex
        """
        ENDPOINT = "recipes/complexSearch"
        URL = f"{cls.ENTRY_POINT}{ENDPOINT}"
        parameters = {
            "includeIngredients": ingredients,
            "sort": "min-missing-ingredients",
            "instructionsRequired": True,
            "fillIngredients": False,
            "addRecipeNutrition": True,  # Also sets addRecipeInformation to True
            "ignorePantry": True,
            "number": number,  # The number of recipes to return.
        }

        spoonacular_response = cls._make_request_and_check_response(
            url=URL,
            parameters=parameters,
            headers=cls.HEADERS,
        )

        return spoonacular_response

    @classmethod
    def get_recipe_from_id(cls, recipe_id: int) -> SpoonacularResponse:
        """
        Gets information about a recipe id. Can be used to validate recipes that users vote on.
        See: https://spoonacular.com/food-api/docs#Get-Recipe-Information
        """
        ENDPOINT = f"recipes/{recipe_id}/information"
        URL = f"{cls.ENTRY_POINT}{ENDPOINT}"
        parameters = {"id": recipe_id, "includeNutrition": False}

        spoonacular_response = cls._make_request_and_check_response(
            url=URL,
            parameters=parameters,
            headers=cls.HEADERS,
        )

        return spoonacular_response

    def get_data(self, retrieval_strategy: DataRetrievalStrategy) -> dict[str, object]:
        """
        Returns response data based on a concrete retrieval_strategy object that inherits from the DataRetrievalStrategy abstract base class.
        """
        retrieved_data = retrieval_strategy.retrieve_data(self.data)

        return retrieved_data
