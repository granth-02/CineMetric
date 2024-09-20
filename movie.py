import requests
import time
import pandas as pd
import aiohttp
import asyncio
import os
import json

async def meta_data(session, api_key, movie_name):
    base_url = ""
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

async def search(mov_names, api_key):
    start_time_total = time.time()
    
    async with aiohttp.ClientSession() as session:
        tasks = []
        for movie_name in mov_names:
            task = asyncio.create_task(process_movie(api_key, session, movie_name))
            tasks.append(task)
        
        user_mov_list = await asyncio.gather(*tasks)

    # Remove None values (failed movie retrievals)
    user_mov_list = [movie for movie in user_mov_list if movie is not None]

    start_time_write = time.time()
    if os.path.exists("User_Data.json"):
        os.remove("User_Data.json")

    with open("User_Data.json", "w") as json_file:  # Open a JSON file for writing
        json.dump(user_mov_list, json_file, indent=4)  # Dump the list of movie data to the JSON file

    df_user_mov = pd.DataFrame(user_mov_list)
    df_user_mov.to_csv("User_Data.csv", index=False)
    end_time_write = time.time()

    end_time_total = time.time()

    print("Movies are stored in User_Data")
    print(f"Total execution time: {end_time_total - start_time_total} seconds")
    print(f"Time taken to use API and collect data: {end_time_write - start_time_write} seconds")


# watched_mov = pd.read_csv("Dhotre_Netflix.csv")
# mov_names = watched_mov['Title']
# api_key = "d1e0e678b2a0325b5a7da373485f3471"
# asyncio.run(search(mov_names, api_key))




# def viz():
#     user_data = pd.read_csv("User_Data.csv")
#     genres = user_data['Genres'].str.split(', ').explode()

#     sns.set_style('dark')   
#     user_data['Count'] = 1

    

    
#     # Graph 1: Release Year of The Movies Watched
#     sns.countplot(x="Release Year", data=user_data, hue="Release Year", palette='magma')
#     plt.title("Distribution of Movies by Release Year")
#     plt.xlabel("Release Year")
#     plt.ylabel("Count")
#     plt.xticks(rotation=45)
#     plt.show()

    
#     # Graph 2: Distribution of Movies Watched by Genre
#     sns.countplot(y=genres, hue=genres, palette='viridis', order=genres.value_counts().index)
#     plt.title("Distribution of Movies by Genre")
#     plt.xlabel("Count")
#     plt.ylabel("Genres")
#     plt.show()

    
#     # Graph 3: Your Genre Preferences Over Time 
#     heatmap_data = user_data.pivot_table(index="Release Year", columns="Genres", values="Count", aggfunc='sum', fill_value=0)
#     sns.heatmap(heatmap_data, cmap="crest", cbar_kws={'label': 'Count of Movies'})
#     plt.title('Your Genre Preferences Over Time (Heatmap)')
#     plt.xlabel('Genre')
#     plt.ylabel('Release Year')
#     plt.show()

    
#     # Graph 4: Genres vs Avg Rating
#     sns.barplot(x="Genres", y="Average Vote", data=user_data, palette='viridis')
#     plt.title("Genres vs Avg Vote")
#     plt.xlabel("Genres")
#     plt.ylabel("Avg Vote")
#     plt.xticks(rotation=45)
#     plt.show()

    
#     # Graph 5: Popularity x Title
#     sns.lineplot(x="Title", y="Average Vote", hue="Count", data=user_data, marker='o')
#     plt.title("Popularity x Title")
#     plt.xlabel("Title")
#     plt.ylabel("Average Vote")
#     plt.xticks(rotation=90)
#     plt.show()


if __name__ == "__main__":
    search()
    





    
