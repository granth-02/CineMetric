from movie import *
from recc import recommend


if __name__ == "__main__":
    movie_titles = search()
    viz()

    user_data = pd.read_csv('User_Data.csv')
    movie_titles = user_data['Title'].tolist()
    for movie_title in movie_titles:
        recommend(movie_title)


