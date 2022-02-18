import pandas as pd
from dataclasses import dataclass
from abc import ABC, abstractmethod


class DataTabulator(ABC):
    """
    Abstract base class for an object that takes in JSON data from Spoonacular and returns a pandas DataFrame.
    """

    @abstractmethod
    def tabulate_data(json_data: list[dict]) -> pd.DataFrame:
        """
        Abstract method for data tabulation strategies.
        """
        pass


@dataclass
class CaloricBreakdownTabulator(DataTabulator):
    """
    Strategy to tabulate macronutrient caloric breakdown profile. Expects nutrition-level data as input.
    """

    field_: str = "caloricBreakdown"

    def tabulate_data(self, json_data: list[dict]) -> pd.DataFrame:
        """
        Extracts the macronutrient percentages from Spoonacular `nutrition` JSON.
        """
        caloric_breakdown = [recipe.get(self.field_) for recipe in json_data]

        return pd.DataFrame(caloric_breakdown)


@dataclass
class NutrientDailyNeedsTabulator(DataTabulator):
    """
    Strategy to tabulate nutrients in terms of percentage of (recommended) daily needs. Expects nutrition-level data as input.
    `nested_pair` expects a key: value pair.
    """

    top_field: str = "nutrients"
    nested_pair: tuple = ("name", "percentOfDailyNeeds")  # (key, value)

    def tabulate_data(self, json_data: list[dict]) -> pd.DataFrame:
        """
        Extracts the nutrient daily need percentages from Spoonacular `nutrition` JSON.
        """
        daily_needs = [
            {
                nutrient[self.nested_pair[0]]: nutrient[self.nested_pair[1]]
                for nutrient in recipe["nutrients"]
            }
            for recipe in json_data
        ]

        return pd.DataFrame(daily_needs)


@dataclass
class InstructionsTabulator(DataTabulator):
    """
    Strategy to tabulate recipe instructions as strings. Expects `analyzedInstructions` data as input.
    """

    first_level: int = 0
    second_level: str = "steps"
    payload_key: str = "step"

    def tabulate_data(self, json_data: list[dict]) -> pd.Series:
        """
        Extracts the nutrient daily need percentages from Spoonacular nutrition JSON.
        """
        all_instructions = []

        for recipe in json_data:
            steps = recipe[self.first_level][self.second_level]
            recipe_instruction_list = []
            # Store the numbered instructions as strings.
            for index, step in enumerate(steps):
                recipe_instruction_list.append(f"{index + 1}. {step[self.payload_key]}")
            # Join the numbered strings in the list with a new line.
            recipe_instructions = "\n".join(recipe_instruction_list)
            all_instructions.append(recipe_instructions)

        return pd.DataFrame(all_instructions, columns=["instructions"])
