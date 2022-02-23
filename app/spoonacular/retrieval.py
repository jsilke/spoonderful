# I could also use protocols, the __call__ method, or functions here too, but I think this annotation is less ambiguous than the alternatives.
from abc import ABC, abstractmethod
from dataclasses import dataclass, field


class DataRetrievalStrategy(ABC):
    """
    Abstract base class for different data retrieval strategies.
    """

    @abstractmethod
    def retrieve_data(self, json_data: dict[str, object]) -> dict[str, object]:
        """
        The abstract method that will implement the data retrieval strategy.
        """
        pass


@dataclass
class SimpleRetrievalStrategy(DataRetrievalStrategy):
    """
    Retrieving recipe data from the SpoonacularResponse produced by `get_recipes_from_ingredients` classmethod.
    """

    fields: tuple = (
        "id",
        "title",
        "usedIngredientCount",
        "missedIngredientCount",
        "likes",
    )

    def retrieve_data(self, json_data: list[dict]) -> list[dict]:
        """
        A concrete data retrieval strategy to extract recipe fields from the response json.
        Retrieves basic information.
        """
        recipe_data = [
            {field: recipe.get(field) for field in self.fields}
            for recipe in json_data.get("results")
        ]

        return recipe_data


class DictRetrievalStrategy(DataRetrievalStrategy):
    """
    Retrieving recipe data from the SpoonacularResponse produced by `get_taste_from_recipe_id` classmethod.
    """

    fields: list = field(default_factory=list)

    def retrieve_data(self, json_data: dict) -> dict:
        """
        A concrete data retrieval strategy to return the taste vector associated with a given recipe.
        """
        return json_data


@dataclass
class ComplexRetrievalStrategy(DataRetrievalStrategy):
    """
    Retrieving recipe data from the SpoonacularResponse produced by the `get_recipes` classmethod.
    TODO implement fields to retrieve based on data.
    """

    fields: tuple = (
        "id",
        "title",
        "image",
        "analyzedInstructions",
        "readyInMinutes",
        "spoonacularScore",
        "aggregateLikes",
        "healthScore",
        "pricePerServing",
        "servings",
        "nutrition",  # nested
        "usedIngredientCount",
        "vegetarian",
        "vegan",
        "glutenFree",
        "dairyFree",
    )

    def retrieve_data(self, json_data: list[dict]) -> list[dict]:
        """
        A concrete data retrieval strategy to extract recipe fields from the response json.
        Retrieves comprehensive information with the restriction that no ingredients are missing (accounts for substitutions).
        """
        recipe_data = [
            {field: recipe.get(field) for field in self.fields}
            for recipe in json_data.get("results")
            if (
                recipe.get("missedIngredientCount") <= 2
            )  # initially 0 tolerance (i.e. `== 0` rather than `<= 2`), but this performed poorly when ingredient lists were short.
        ]

        return recipe_data
