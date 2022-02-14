# Meal recommendation for food waste reduction

### Use case
---

The goal of this project is to build a meal recommender with the principal intention of mitigating food waste by prioritizing ingredients that the user already has in their possession. This is the core nuance that differentiates this project from other meal planners. While other factors including cost, variety, and nutrition will be considered in recommendations, priority will be given to recipes composed of household ingredients.

### Data
---

Most data is dynamically sourced from [Spoonacular](https://spoonacular.com/)'s API in accordance with their [terms of use](https://spoonacular.com/food-api/terms). Note that the Spoonacular team also provides a list including the 1000 most popular ingredients and their associated IDs [here](https://spoonacular.com/food-api/docs#List-of-Ingredients). Direct use of this project's source code will require an API key, which can be obtained [directly from Spoonacular](https://spoonacular.com/food-api/console#Dashboard) or [through RapidAPI](https://rapidapi.com/spoonacular/api/recipe-food-nutrition/), though this project is structured to use a RapidAPI key for authentication.

***Note:*** As of 2022/02/13, the versions of the API hosted by Spoonacular and RapidAPI differ in functionality and recipe IDs are not reliably synchronous between the two. This may change in the future.

### Key Outputs
---

This project uses a list of household ingredients to generate top meal recommendations for the user through a combination of content-based and collaborative filtering strategies.