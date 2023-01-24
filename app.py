import streamlit as st
import pickle
import requests
import pandas as pd

footer="""<style>
a:link , a:visited{
color: black;
background-color: transparent;
}

a:hover,  a:active {
color: red;
background-color: transparent;
}

.footer {
position: fixed;
left: 0;
bottom: 0;
width: 100%;
background-color: white;
color: black;
text-align: center;
}
</style>
<div class="footer">
<p>Developed with <span style ='color:red'>❤</span> by <a href="https://shrikrishnaparab.tech/" target="_blank">Shrikrishna Parab</a></p>
</div>
"""

def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    #homepage_path = data['homepage']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path

def get_popular(qualified):
    #print(qualified.head())
    top_5 = qualified.head(5)
    return top_5


def top_genre_based_movies(genre, percentile=0.95):
    df = genre_df[genre_df['genres'].str.contains(genre)]
    vote_counts = df['vote_count'].astype('int')
    vote_averages = df['vote_average'].astype('int')
    C = vote_averages.mean()
    m = vote_counts.quantile(percentile)
    qualified = df[(df['vote_count'] >= m)][['movie_id', 'title', 'vote_count', 'vote_average', 'genres']]
    qualified['vote_count'] = qualified['vote_count'].astype('int')
    qualified['vote_average'] = qualified['vote_average'].astype('int')
    qualified['wr'] = qualified.apply(
        lambda x: (x['vote_count'] / (x['vote_count'] + m) * x['vote_average']) + (m / (m + x['vote_count']) * C),
        axis=1)
    qualified = qualified.sort_values('wr', ascending=False).head(250)
    return qualified

def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    homepage_path_list = []
    for i in distances[1:6]:
        # fetch the movie poster
        movie_id = movies.iloc[i[0]].movie_id
        full_path= fetch_poster(movie_id)
        #homepage_path_list.append(homepage_path)
        recommended_movie_posters.append(full_path)
        recommended_movie_names.append(movies.iloc[i[0]].title)

    return recommended_movie_names,recommended_movie_posters


st.title("Movie Recommender System")

movies = pickle.load(open('movie_list_hi.pkl','rb'))
similarity = pickle.load(open('similarity_hi.pkl','rb'))
all_movies = pickle.load(open('movies_df_hi.pkl','rb'))
top_popular = pickle.load(open('top_popular_hi.pkl','rb'))

s = all_movies.apply(lambda x: pd.Series(x['genres']),axis=1).stack().reset_index(level=1, drop=True)
s.name = 'genres'
genre_df = all_movies.drop('genres', axis=1).join(s)

movie_list = movies['title'].values
option_selected = st.selectbox(
    'Type or Select Movie Name from Dropdown',
    movie_list
)

genre_list = ['Action','Romance','Adventure','Science Fiction','Comedy']
genre_selected = st.selectbox(
    'Type or Select Genre from Dropdown',
    genre_list
)

if st.button('Show Recommendation'):
    recommended_movie_names, recommended_movie_posters = recommend(option_selected)
    top_popular_movies = get_popular(top_popular)
    st.header("Movies Based on Content: Similar Movies")
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.image(recommended_movie_posters[0], caption=recommended_movie_names[0])
    with col2:
        st.image(recommended_movie_posters[1], caption=recommended_movie_names[1])

    with col3:
        st.image(recommended_movie_posters[2], caption=recommended_movie_names[2])
    with col4:
        st.image(recommended_movie_posters[3], caption=recommended_movie_names[3])
    with col5:
        st.image(recommended_movie_posters[4], caption=recommended_movie_names[4])

    st.header("Movies Based on Popularity: Top Popular")
    popular = []
    for row in top_popular_movies.loc[:,['title','movie_id']].values:
        popular.append(row)
    col6, col7, col8, col9, col10 = st.columns(5)
    with col6:
        full_path = fetch_poster(popular[0][1])
        st.image(full_path, caption=popular[0][0])
    with col7:
        full_path = fetch_poster(popular[1][1])
        st.image(full_path, caption=popular[1][0])
    with col8:
        full_path = fetch_poster(popular[2][1])
        st.image(full_path, caption=popular[2][0])
    with col9:
        full_path = fetch_poster(popular[3][1])
        st.image(full_path, caption=popular[3][0])
    with col10:
        full_path = fetch_poster(popular[4][1])
        st.image(full_path, caption=popular[4][0])


    st.header("Movies Based on Genre: Top "+str(genre_selected)+" Movies")
    top_gener_based = top_genre_based_movies(genre_selected).head(5)
    genre_popular = []
    for row in top_gener_based.loc[:, ['title', 'movie_id']].values:
        genre_popular.append(row)
    col11, col12, col13, col14, col15 = st.columns(5)
    with col11:
        full_path = fetch_poster(genre_popular[0][1])
        st.image(full_path, caption=genre_popular[0][0])
    with col12:
        full_path = fetch_poster(genre_popular[1][1])
        st.image(full_path, caption=genre_popular[1][0])
    with col13:
        full_path = fetch_poster(genre_popular[2][1])
        st.image(full_path, caption=genre_popular[2][0])
    with col14:
        full_path = fetch_poster(genre_popular[3][1])
        st.image(full_path, caption=genre_popular[3][0])
    with col15:
        full_path = fetch_poster(genre_popular[4][1])
        st.image(full_path, caption=genre_popular[4][0])









st.markdown(footer,unsafe_allow_html=True)
