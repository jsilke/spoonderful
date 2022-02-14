import pandas as pd
from dataclasses import dataclass
from abc import ABC, abstractmethod


class NutritionTabulator(ABC):
    """
    Abstract base class for an object that takes in nutrition JSON data from Spoonacular and returns a pandas DataFrame.
    """

    @abstractmethod
    def tabulate_nutrition(json_nutrition_data: list[dict]) -> pd.DataFrame:
        """
        Abstract method for nutrition data tabulation strategies.
        """
        pass


@dataclass
class CaloricBreakdownTabulator(NutritionTabulator):
    """
    Strategy to tabulate macronutrient caloric breakdown profile.
    """

    field_: str = "caloricBreakdown"

    def tabulate_nutrition(self, json_nutrition_data: list[dict]) -> pd.DataFrame:
        """
        Extracts the macronutrient percentages from Spoonacular nutrition JSON.
        """
        caloric_breakdown = [recipe.get(self.field_) for recipe in json_nutrition_data]

        return pd.DataFrame(caloric_breakdown)


@dataclass
class NutrientDailyNeedsTabulator(NutritionTabulator):
    """
    Strategy to tabulate nutrients in terms of percentage of (recommended) daily needs.
    `nested_pair` expects a key: value pair.
    """

    top_field: str = "nutrients"
    nested_pair: tuple = ("name", "percentOfDailyNeeds")  # (key, value)

    def tabulate_nutrition(self, json_nutrition_data: list[dict]) -> pd.DataFrame:
        """
        Extracts the nutrient daily need percentages from Spoonacular nutrition JSON.
        """
        daily_needs = [
            {
                nutrient[self.nested_pair[0]]: nutrient[self.nested_pair[1]]
                for nutrient in recipe["nutrients"]
            }
            for recipe in json_nutrition_data
        ]

        return pd.DataFrame(daily_needs)
