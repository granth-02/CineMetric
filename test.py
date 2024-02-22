import aiohttp
import asyncio
import time
import pandas as pd
import os
import math

async def meta_data(session, api_key, movie_name):
    base_url = "https://api.themoviedb.org/3/search/movie"
    parameters = {
        "api_key": api_key,
        "query": movie_name,
    }
    async with session.get(base_url, params=parameters) as response:
        meta_data = await response.json()
        if 'results' in meta_data and meta_data['results']:
            movie_id = meta_data['results'][0]['id']
            movie_details_url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}&append_to_response=credits"
            async with session.get(movie_details_url) as details_response:
                details = await details_response.json()
                return details
        else:
            return None

async def process_movie(api_key, movie_name):
    async with aiohttp.ClientSession() as session:
        return await meta_data(session, api_key, movie_name)

async def search(movie_names, api_key):
    async with aiohttp.ClientSession() as session:
        start_time_total = time.time()

        start_time_filter = time.time()
        tasks = [process_movie(api_key, movie_name) for movie_name in movie_names if isinstance(movie_name, str)]
        results = await asyncio.gather(*tasks)
        end_time_filter = time.time()

        user_mov_list = [result for result in results if result is not None]

        start_time_write = time.time()
        if os.path.exists("User_Data.csv"):
            os.remove("User_Data.csv")

        df_user_mov = pd.DataFrame(user_mov_list)
        df_user_mov.to_csv("User_Data.csv", index=False)
        end_time_write = time.time()

        end_time_total = time.time()

        print("Movies are stored in User_Data")
        print(f"Total execution time: {end_time_total - start_time_total} seconds")
        print(f"Time taken to filter data: {end_time_filter - start_time_filter} seconds")
        print(f"Time taken to use API and collect data: {end_time_write - start_time_write} seconds")

# Load movie names from CSV and pass them to the search function
watched_mov = pd.read_csv("Dhotre_Netflix.csv")
mov_names = watched_mov['Title'].tolist()
api_key = "d1e0e678b2a0325b5a7da373485f3471"
asyncio.run(search(mov_names, api_key))
