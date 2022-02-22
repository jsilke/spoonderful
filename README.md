[![License](https://img.shields.io/github/license/jsilke/spoonderful)](./LICENSE)
![Issues](https://img.shields.io/github/issues/jsilke/spoonderful)
![Last Commit](https://img.shields.io/github/last-commit/jsilke/spoonderful)

# **Recipe recommendation for food waste reduction**

## **Top Contributors**

  * Jordan Silke [![GitHub](https://img.shields.io/github/followers/jsilke?style=social)](https://github.com/jsilke)

### **Use case**

The goal of this project is to build a recipe recommender with the principal intention of mitigating food waste by prioritizing ingredients that the user already has in their possession. This is the core nuance that differentiates this project from other meal planners. While other factors including cost, variety, and nutrition will be considered in recommendations, priority will be given to recipes composed of household ingredients.

### **Data**

Most data is dynamically sourced from [Spoonacular](https://spoonacular.com/)'s API in accordance with their [terms of use](https://spoonacular.com/food-api/terms). Note that the Spoonacular team also provides a list including the 1000 most popular ingredients and their associated IDs [here](https://spoonacular.com/food-api/docs#List-of-Ingredients). Direct use of this project's source code will require an API key, which can be obtained [directly from Spoonacular](https://spoonacular.com/food-api/console#Dashboard) or [through RapidAPI](https://rapidapi.com/spoonacular/api/recipe-food-nutrition/), though this project is structured to use the version of the API hosted by RapidAPI.

### **Project Structure**

```bash
.
│   .env # Needs to be created by the user. These variables are used in config.py
│   .gitignore
│   alembic.ini
│   environment.yml # requirements to import for conda users.
│   LICENSE # MIT
│   README.md
│   requirements.txt # requirements to import for venv users.
│
├───alembic # Database migration tool
│   │   env.py
│   │   README
│   │   script.py.mako
│   │
│   └───versions
└───app
    │   __init__.py
    │
    ├───spoonacular # Handles spoonacular responses for data sourcing.
    │   response.py
    │   retrieval.py       
    │
    └───spoonderful # Core application.
        │   config.py
        │   main.py
        │
        ├───auth # JWT
        │   oauth2.py
        │   utils.py
        │
        ├───data # Pydantic schemas for validation and SQLAlchemy models for user data.
        │   database.py
        │   models.py
        │   schemas.py   
        │
        ├───processing # Processing Spoonacular JSON data
        │   pipeline.py
        │   preprocess.py
        │   tabulation.py        
        │
        └───routes # API routers.
            login.py
            recommendation.py
            register.py
            user.py
            vote.py
```
## ***How to use this project***
---
Users of conda can recreate the environment by importing [environment.yml](./environment.yml) and venv users can user [requirements.txt](./requirements.txt). Note that this project was developed on a Windows 10 machine and, as such, the requirement versions may need to be removed along with Windows-specific dependencies to get the project running locally. These requirements also assume that you will be using PostgreSQL as your RDBMS and that it is already installed and configured.

Once you have your environment setup, you will need to obtain an API key from [RapidAPI](https://rapidapi.com/spoonacular/api/recipe-food-nutrition/) and configure your .env file. Note that as this file must contain secrets, be sure to keep it in the provided .gitignore or move .env to another directory to prevent accidental upload. You should also create a database with the same name you used in your .env file; the tables will be generated automatically by SQLAlchemy.

With a properly configured virtual environment and .env file, simply activate the virtual environment, ensure that you are in the project route directory in your terminal, and run the following command:

```bash
uvicorn app.spoonderful.main:app
```

The application should now be running locally, and the interactive documentation should be available in your browser at:
http://127.0.0.1:8000/docs

***TL;DR*** import the requirements, setup your database and .env file to match expected [settings](./config.py), then run `uvicorn app.spoonderful.main:app` in your environment and play around with the API @ http://127.0.0.1:8000/docs

### **Data Pipeline**

The API currently supports two recommendation approaches. The trivial (`simple`) approach simply returns the top 5 (or fewer) results from Spoonacular's recipe search that you aren't missing any ingredients to make. 

The `varied` approach first filters the top 100 results to a set with no missing ingredients. If the remaining number of recipes in this set is five or fewer, the results are returned; otherwise, the dimensionality of the feature space is reduced to two principal components and dynamic k-means clustering
is applied to force five recipe clusters. The recipes that are closest to the centroid in each cluster are then returned as the top five recommendations.