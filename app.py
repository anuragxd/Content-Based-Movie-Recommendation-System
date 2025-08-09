import streamlit as st
import pickle
import pandas as pd
import requests

import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("TMDB_API_KEY")

def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}&language=en-US"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        poster_path = data.get('poster_path')
        
        if not poster_path:
            return "https://via.placeholder.com/500x750?text=No+Image+Available"
        
        return f"https://image.tmdb.org/t/p/w500/{poster_path}"
    
    except requests.exceptions.RequestException as e:
        print(f"Error fetching poster for movie ID {movie_id}: {e}")
        return "https://via.placeholder.com/500x750?text=Error"


def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_titles = []
    recommended_posters = []

    for i in movie_list:
        movie_id = movies.iloc[i[0]]['movie_id']  # FIXED HERE
        recommended_titles.append(movies.iloc[i[0]]['title'])
        recommended_posters.append(fetch_poster(movie_id))

    return recommended_titles, recommended_posters

# Load data
movie_list = pickle.load(open('movies_dict.pkl', 'rb'))
movies = pd.DataFrame(movie_list)
similarity = pickle.load(open('similarity.pkl', 'rb'))

# Streamlit UI
st.title("🎬 Movie Recommender System")

selected_movie = st.selectbox(
    "Select a movie",
    movies['title'].values
)

if st.button("Show Recommendations"):
    names, posters = recommend(selected_movie)
    
    cols = st.columns(5)
    for i in range(5):
        with cols[i]:
            st.text(names[i])
            st.image(posters[i])
