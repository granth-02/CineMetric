from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd

user_data = pd.read_csv('User_Data.csv')
app = FastAPI()

origins = [
    'http://localhost:3000'
]
app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_credentials = True,
    allow_methods=["*"],
    allow_headers = ["*"],
)

@app.get('/graph')
async def data():
    movie_data = []
    for index, row in user_data.iterrows():
        
        import_data = {
           "Title": row["Title"],
            "Release Year": row["Release Year"],
            "Average Vote": row["Average Vote"],
            "Popularity": row["Popularity"],
            "Genres": row["Genres"],
            "Cast": row["Cast"],
            "Director": row["Director"]
        }
        movie_data.append(import_data)

    return movie_data

@app.get("/")
async def root():
    return {"message": "Hello World"}