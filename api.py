from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import json
import math
from recc import recommend

# Load data from JSON file
with open('User_Data.json', 'r') as file:
    user_data = json.load(file)

app = FastAPI()

origins = [
    'http://localhost:3000'
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def sanitize_data(data):
    for key, value in data.items():
        if isinstance(value, float) and math.isnan(value):
            data[key] = None
    return data

@app.get('/graph')
async def data():
    movie_data = []
    for row in user_data:
        import_data = {
            "Title": row["Title"],
            "Release Year": row["Release Year"],
            "Average Vote": row["Average Vote"],
            "Popularity": row["Popularity"],
            "Genres": row["Genres"],
            "Cast": row["Cast"],
            "Director": row["Director"]
        }
        sanitized_data = sanitize_data(import_data)
        movie_data.append(sanitized_data)

    return movie_data

@app.get("/recc")
async def recc():
    with open('all_recommendations.json', 'r') as file:
        reccomendations = json.load(file)
    return {'reccomendations': reccomendations}

@app.get("/")
async def root():
    return {"message": "Hello World"}
