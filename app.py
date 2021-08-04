import streamlit as st
import pickle
import pandas as pd
import requests


st.title('Movie Recommender System')

movies_dict = pickle.load(open('movies_dict.pkl','rb'))
movies = pd.DataFrame(movies_dict)

similarity = pickle.load(open('similarity.pkl','rb'))

def get_poster(movie_id):
    data = requests.get("https://api.themoviedb.org/3/movie/{}?api_key=5625e2b25f4cebf3d7ec79aa01086073&language=en-US".format(movie_id))
    poster = data.json()
    poster_path = poster['poster_path']
    return "https://image.tmdb.org/t/p/w500/" + poster_path


def recommend(movie):
    movie_index = movies[movies['title']==movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)),reverse=True,key= lambda x:x[1])[1:6]
    
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_names.append(movies.iloc[i[0]].title)
        recommended_movie_posters.append(get_poster(movie_id))
    return recommended_movie_names,recommended_movie_posters


selected_movie = st.selectbox(
'Type or select a movie',
movies['title'].values)

if st.button('Recommend'):
    recommended_movie_names,recommended_movie_posters = recommend(selected_movie)
    col1, col2, col3, col4, col5 = st.beta_columns(5)
    with col1:
        st.text(recommended_movie_names[0])
        st.image(recommended_movie_posters[0])
    with col2:
        st.text(recommended_movie_names[1])
        st.image(recommended_movie_posters[1])

    with col3:
        st.text(recommended_movie_names[2])
        st.image(recommended_movie_posters[2])
    with col4:
        st.text(recommended_movie_names[3])
        st.image(recommended_movie_posters[3])
    with col5:
        st.text(recommended_movie_names[4])
        st.image(recommended_movie_posters[4])