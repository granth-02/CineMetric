import numpy as np
import pandas as pd
import ast
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import nltk
from nltk.stem.porter import PorterStemmer
import json
import os
import requests


credits_df = pd.read_csv("10000 Credits Data.csv") # Credits
movies_df = pd.read_csv("10000 Movies Data.csv")   # Movies

# Merging the data
movies_df = movies_df.merge(credits_df, on='title')

# Selecting specific columns
movies_df = movies_df[['title', 'overview', 'Genres', 'Keywords', 'Cast', 'Crew', 'popularity', 'vote_average']]

# Convert string representations of lists to actual lists
features = ["Genres", "Keywords", "Cast", "Crew"]
for feature in features:
    movies_df[feature] = movies_df[feature].apply(ast.literal_eval)

# Function to extract genre names
def extract_genre_names(Genres):
    if isinstance(Genres, list):
        return [genre['name'] for genre in Genres]
    return []

# Function to extract director and top 3 actors/actresses
def get_dir(Crew):
    for member in Crew:
        if member['job'] == 'Director':
            return member['name']
    return np.nan

def get_act(Cast):
    if isinstance(Cast, list):
        names = [actor['name'] for actor in Cast]
        if len(names) > 3:
            return names[:3]
        return names
    return []

# Clean data
def clean(obj):
    if isinstance(obj, list):
        return obj
    elif isinstance(obj, str):
        return obj.lower().replace(" ", "")
    else:
        return ''

movies_df['director'] = movies_df['Crew'].apply(get_dir)
movies_df['Cast'] = movies_df['Cast'].apply(get_act)
movies_df['Genres'] = movies_df['Genres'].apply(extract_genre_names)
movies_df['Keywords'] = movies_df['Keywords'].apply(clean)
movies_df['director'] = movies_df['director'].apply(clean)

# Function to create soup
def create_soup(row):
    
    
    keywords = ' '.join([keyword['name'] for keyword in row['Keywords']]) if isinstance(row['Keywords'], list) else ''
    cast = ' '.join(row['Cast']) if isinstance(row['Cast'], list) else ''
    director = row['director'] if isinstance(row['director'], str) else ''
    genres = ' '.join(row['Genres']) if isinstance(row['Genres'], list) else ''
    popularity = str(row['popularity']) if 'popularity' in row else ''
    vote_average = str(row['vote_average']) if 'vote_average' in row else ''
    
    return keywords + ' ' + cast + ' ' + director + ' ' + genres + ' ' + popularity + ' ' + vote_average

movies_df["soup"] = movies_df.apply(create_soup, axis=1)

# CountVectorizer
cv = CountVectorizer(stop_words='english')
vectors = cv.fit_transform(movies_df['soup']).toarray()

# Stemming
ps = PorterStemmer()
def stem(txt):
    return ' '.join([ps.stem(word) for word in txt.split()])

movies_df['soup'] = movies_df['soup'].apply(stem)

# Cosine Similarity
similar = cosine_similarity(vectors)

TMDB_API_KEY = "d1e0e678b2a0325b5a7da373485f3471"
TMDB_BASE_URL = "https://api.themoviedb.org/3"
POSTER_BASE_URL = "https://image.tmdb.org/t/p/w500"  # Change w500 to adjust poster size if needed

# Recommendation function
def recommend(movie_title):
    mov_index = movies_df[movies_df['title'] == movie_title].index
    if len(mov_index) == 0:
        print("Movie not found.")
        return []
    mov_index = mov_index[0]
    score = similar[mov_index]
    similar_movies = sorted(list(enumerate(score)), reverse=True, key=lambda x: x[1])[1:11]
    print("\nWatched Movie:", movie_title)
    print("Similar Movies: \n")
    recommendations = []
    recc_titles = set()
    for i, _ in similar_movies:
        title = movies_df.iloc[i]['title']
        votes = movies_df.iloc[i]['vote_average']
        # Fetch movie details from TMDb API to get the poster URL
        try:
            response = requests.get(f"{TMDB_BASE_URL}/search/movie", 
                                    params={"api_key": TMDB_API_KEY, "query": title})
            data = response.json()
            poster_path = data["results"][0]["poster_path"] if data["results"] else None
            poster_url = POSTER_BASE_URL + poster_path if poster_path else None
        except Exception as e:
            print(f"Error fetching movie details for {title}: {e}")
            poster_url = None

        if title not in recc_titles:
            print(f"{title} (Rating: {votes})")
            recc_titles.add(title)
            recommendations.append({"Title": title, "Rating": votes, "PosterURL": poster_url})
        else:
            continue 
    return recommendations





