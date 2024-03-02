from movie import search
# from recc import recommend
import asyncio
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

    # user_data = pd.read_csv('User_Data.csv')
    # movie_titles = user_data['Title'].tolist()
    # for movie_title in movie_titles:
    #     recommend(movie_title)


