# Import python libraries
import pickle
import numpy as np
import pandas as pd
import streamlit as st
import requests
from PIL import Image
# Import file
data=pd.read_csv('recipes_w_clusters.csv')
# Import user modules
#from functions import cleanOperation, cleankSymbol, cleanDuration, preprocess
from IPython.display import display

with open("spoonacular-api-key.txt", "r") as file:
    api_key = file.readline().split(':')[1].strip()



#################

def get_recipe_id(recipe_title):
    endpoint = 'https://api.spoonacular.com/recipes/complexSearch'
    params = {
        'apiKey': api_key,
        'query': recipe_title
    }
    response = requests.get(endpoint, params=params)
    if response.status_code == 200:
        results = response.json()
        if results:
            return results['results'][0]['id']  # the first recipe is the one we want
    return None

def get_recipe_instructions(recipe_title):
    recipe_id = get_recipe_id(recipe_title)
    if recipe_id:
        endpoint = f'https://api.spoonacular.com/recipes/{recipe_id}/information'
        params = {
            'apiKey': api_key
        }
        response = requests.get(endpoint, params=params)
        
        if response.status_code == 200:
            recipe_info = response.json()
            return recipe_info.get('instructions', 'Instructions not available.')
            return recipe_info
    return "Mamma mia! I cannot find my cookbook for this one."

##################

def print_recipe_details(recipe_title):
    # Ideally, replace this function with your logic to fetch details about the selected recipe
        #display(selected_recipe)
    selected_recipe = data[data['title'] == recipe_title].head(1)
    if len(selected_recipe) > 0:
        # Display the details of the selected recipe
        print("\nBelow are some details about this recipe (but who cares about health anyway):")
        for index, row in selected_recipe.iterrows():
            st.write(row['title'])
            st.write(f"Health Score (out of 100): {row['healthScore']}")
            st.write(f"Price Per Serving: ${row['pricePerServing']}")
            
    else: st.write("Mamma mia! I cannot find my cookbook for this one")

##################

def suggest_recipes():
    with open("spoonacular-api-key.txt", "r") as file:
        api_key = file.readline().split(':')[1].strip()
    endpoint = 'https://api.spoonacular.com/recipes/findByIngredients'

    # Get the ingredients from the user
    user_input = st.text_input("1. Enter the ingredients in your fridge or pantry (comma-separated): ")
    fridge_contents = user_input.split(',') if user_input else []

    # Define parameters for the request
    params = {
        'ingredients': ','.join(fridge_contents),
        'apiKey': api_key
    }

    response = requests.get(endpoint, params=params)

    if response.status_code == 200:
        recipes = response.json()
        # Convert the recipe data to a DataFrame
        recipe_data = []
        for recipe in recipes:
            recipe_data.append({
                'RECIPES! Here is my TOP Picks that include your ingredients': recipe['title'],
                'INGREDIENTS: You will need to add those': ', '.join([ingredient['name'] for ingredient in recipe['missedIngredients']])
            })
        recipes_df = pd.DataFrame(recipe_data)
        st.write(recipes_df)

#### Prompt the user to select a preferred recipe
        selected_recipe_title = st.text_input("2. Which of those recipes do you prefer? Copy-paste your favorite recipe title (case sensitive): ")
        instructions=get_recipe_instructions(selected_recipe_title)
        instructions=instructions.replace("<ol><li>","").replace("</li></ol>","")
        st.markdown(instructions)
        
        selected_recipe = data[data['title'] == selected_recipe_title].head(1)
        
        if len(selected_recipe) > 0:
            st.write("## Love your choice. Here are some details about your preferred recipe:")
            print_recipe_details(selected_recipe_title)
        
            
### Suggest another recipe from the model
        
        # Get cluster number of the selected recipe
            selected_cluster = selected_recipe.iloc[0]['cluster']
            # Filter data for recipes in the same cluster as the selected recipe
            cluster_recipes = data[data['cluster'] == selected_cluster]
        
            # Remove the selected recipe from the cluster if it exists
            cluster_recipes = cluster_recipes[cluster_recipes['title'] != selected_recipe_title]
           # Choose a random recipe from the same cluster
            random_recommendation = cluster_recipes.sample(1)
            st.write("## Given your fine taste, may I risk a suggestion?")
            print_recipe_details(random_recommendation['title'].iloc[0])
            
        else:st.write("## Excellent choice !")
        
    else:
        # Print an error message if the request was not successful
        st.write('Error:', response.status_code)

# Run the app
if __name__ == '__main__':
    suggest_recipes()



