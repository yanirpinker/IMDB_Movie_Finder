import streamlit as st
import requests

# Your TMDb API key
tmdb_api_key = 'a8f5f757f3f5ad1ab531dcc4a5018108'

# Define Monday.com-style colors
monday_bg_color = "#F6F8FA"
monday_primary_color = "#0073E6"
monday_secondary_color = "#4B4B4B"

# Apply Monday.com-style UI
st.markdown(
    f"""
    <style>
    .stApp {{
        background-color: {monday_bg_color};
    }}
    .stSlider > div {{
        color: {monday_primary_color};
    }}
    .stCheckbox > div {{
        color: {monday_primary_color};
    }}
    .stButton > button {{
        background-color: {monday_primary_color};
        color: white;
        border-radius: 12px;
        padding: 10px 20px;
        border: none;
        font-size: 16px;
    }}
    .stButton > button:hover {{
        background-color: {monday_secondary_color};
    }}
    .stSelectbox > div, .stMultiSelect > div {{
        color: {monday_primary_color};
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# Function to fetch movie data from TMDb API
def fetch_tmdb_movies(genre_id, year_range, rating_range, tmdb_api_key):
    url = (
        f"https://api.themoviedb.org/3/discover/movie?"
        f"api_key={tmdb_api_key}&"
        f"with_genres={genre_id}&"
        f"primary_release_date.gte={year_range[0]}-01-01&"
        f"primary_release_date.lte={year_range[1]}-12-31&"
        f"vote_average.gte={rating_range[0]}&"
        f"vote_average.lte={rating_range[1]}&"
        f"sort_by=vote_average.desc"
    )
    response = requests.get(url)
    if response.status_code == 200:
        return response.json().get('results', [])
    else:
        return []

# Fetch TMDb genres
def fetch_tmdb_genres(tmdb_api_key):
    url = f"https://api.themoviedb.org/3/genre/movie/list?api_key={tmdb_api_key}&language=en-US"
    response = requests.get(url)
    if response.status_code == 200:
        genres = response.json().get('genres', [])
        return {genre['name']: genre['id'] for genre in genres}
    else:
        return {}

# Streamlit UI components with enhanced style
st.title("🎬 Find Your Next Movie")

st.subheader("Specify Your Preferences")

# 1. Fetch and display genres from TMDb
genres = fetch_tmdb_genres(tmdb_api_key)
selected_genres = st.multiselect('Select Genre(s):', list(genres.keys()))

# 2. Release Year (Mandatory)
year_range = st.slider('Select Release Year Range:', 1920, 2024, (2020, 2024))

# 3. IMDb Rating (Mandatory)
rating_range = st.slider('Select IMDb Rating Range:', 7.0, 10.0, (7.0, 10.0))

# 4. Star (Optional)
selected_stars = st.text_input('Enter a Star Name (optional):')

# Collecting movie data from TMDb API
top_movies = []
for genre_name in selected_genres:
    genre_id = genres[genre_name]
    movies = fetch_tmdb_movies(genre_id, year_range, rating_range, tmdb_api_key)
    if selected_stars:
        # Filter by star name if provided
        movies = [movie for movie in movies if selected_stars.lower() in (movie.get('overview', '')).lower()]
    top_movies.extend(movies)
    if len(top_movies) >= 3:
        break

# Display the results
if top_movies:
    st.write(f"### Top {len(top_movies)} Movies Matching Your Criteria")
    for movie in top_movies[:3]:  # Limit to top 3 movies
        st.subheader(f"{movie['title']} ({movie['release_date'][:4]})")
        poster_path = movie['poster_path']
        if poster_path:
            st.image(f"https://image.tmdb.org/t/p/w500{poster_path}", width=150)
        # Ensure the rating is displayed correctly
        rating = movie.get('vote_average', 'N/A')
        st.write(f"**TMDb Rating:** {rating}")
        st.write(f"**Overview:** {movie['overview']}")
        youtube_search_url = f"https://www.youtube.com/results?search_query={movie['title']}+trailer"
        st.write(f"[Watch Trailer on YouTube]({youtube_search_url})")
        st.write("---")
else:
    st.write("No movies found matching your criteria.")
