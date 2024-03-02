from movie import search
from recc import recommend
import asyncio
import json
import os
import pandas as pd

async def main():
    watched_mov = pd.read_csv("Dhotre_Netflix.csv")
    mov_names = watched_mov['Title']
    api_key = "d1e0e678b2a0325b5a7da373485f3471"
    await search(mov_names, api_key)


if __name__ == "__main__":
    # movie_titles = 
    asyncio.run(main())
    # viz()

    all_recommendations = []


    with open('User_Data.json', 'r') as file:
        user_data = json.load(file)

    movie_titles = [entry['Title'] for entry in user_data]


    for movie_title in movie_titles:
        recommendations = recommend(movie_title)
        all_recommendations.extend(recommendations)


    if os.path.exists("all_recommendations.json"):
        os.remove("all_recommendations.json")

    with open('all_recommendations.json', 'w') as file:
        json.dump(all_recommendations, file, indent=4)

    


