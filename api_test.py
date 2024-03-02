import requests
import time
import pandas as pd
import aiohttp
import asyncio
import os
import json
from typing import List, Dict
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()


async def meta_data(session, api_key, movie_name):
    base_url = "https://api.themoviedb.org/3/search/movie"
    parameters = {
        "api_key": api_key,
        "query": movie_name,
    }
    
    # Convert NaN values to a placeholder
    parameters = {k: v if pd.notna(v) else '' for k, v in parameters.items()}
    
    async with session.get(base_url, params=parameters) as response:
        meta_data = await response.json()
        
        if meta_data['results']:
            movie_id = meta_data['results'][0]['id']
            movie_details_url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}&append_to_response=credits"
            
            async with session.get(movie_details_url) as response_details:
                details = await response_details.json()
                return details
        else:
            return None

async def process_movie(api_key, session, movie_name):
    movie_details = await meta_data(session, api_key, movie_name)
    if movie_details is None:
        return None
    
    if 'Season' in movie_details.get('title', '') or 'Limited Series' in movie_details.get('title', ''):
        return None

    director = next((crew['name'] for crew in movie_details.get('credits', {}).get('crew', []) if crew['job'] == 'Director'), 'N/A')
    release_year = movie_details.get('release_date', 'N/A')[:4]
    return {
        "Title": movie_details.get('title', 'N/A'),
        "Overview": movie_details.get('overview', 'N/A'),
        "Release Year": release_year,
        "Runtime(Mins)": movie_details.get('runtime', 'N/A'),
        "Average Vote": movie_details.get('vote_average', 'N/A'),
        "Popularity": movie_details.get('popularity', 'N/A'),
        "Genres": ", ".join([genre['name'] for genre in movie_details.get('genres', [])[:1]]),
        "Cast": ", ".join(actor['name'] for actor in movie_details.get('credits', {}).get('cast', [])[:5]),
        "Director": director
    }

@app.get("/movies")
async def get_movies(api_key: str, movies: List[str]):
    async with aiohttp.ClientSession() as session:
        tasks = [process_movie(api_key, session, movie_name) for movie_name in movies]
        user_mov_list = await asyncio.gather(*tasks)

    return user_mov_list