import streamlit as st
import pandas as pd
import pickle
import requests
import gdown

def fetch_poster(movie_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=79debb0f5cf44084dc72bfb673b061f8&language-en-US'.format(movie_id), verify=False)
    data = response.json()
    # st.text(data)
    # st.text('https://api.themoviedb.org/3/movie/{}?api_key=79debb0f5cf44084dc72bfb673b061f8&&language=en-US'.format(movie_id))
    return "https://image.tmdb.org/t/p/w185" + data['poster_path']

def recommend(movie):
    movie_index = movie_df[movie_df['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list_sorted = sorted(list(enumerate(distances)), reverse=True, key=lambda x:x[1])[1:6]

    recommended_movies = []
    recommended_movie_posters = []
    
    for i in movies_list_sorted:
        recommended_movies.append(movie_df.iloc[i[0]].title)
        movie_id = movie_df.iloc[i[0]].id
        recommended_movie_posters.append(fetch_poster(movie_id))
        # fetch poster from API
    return recommended_movies, recommended_movie_posters


movies_list = pickle.load(open('movies.pkl', 'rb'))
movie_df = pd.DataFrame(movies_list)
movies_list1 = movies_list['title'].values



# similarity = pickle.load(open('similarity.pkl', 'rb'))
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

cv = CountVectorizer(max_features=5000, stop_words='english')
vectors = cv.fit_transform(movie_df['tag']).toarray()
similarity = cosine_similarity(vectors)



st.title("Movie Recommender System")

seelcted_movie_name = st.selectbox(
    "Please select your favourite movie",
    movies_list1
)

if st.button('Show Recommendation'):
    recommended_movie_names,recommended_movie_posters = recommend(seelcted_movie_name)
    col1, col2, col3, col4, col5 = st.columns(5)
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