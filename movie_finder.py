import streamlit as st
import requests

# Your OMDb API key
api_key = '2f2ea8fd'

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

# Function to fetch movie data from OMDb API
def fetch_movie_data(title, year, api_key):
    url = f"http://www.omdbapi.com/?t={title}&y={year}&apikey={api_key}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None

# Streamlit UI components with enhanced style
st.title("🎬 Find Your Next Movie")

st.subheader("Specify Your Preferences")

# 1. Release Year (Mandatory)
year_range = st.slider('Select Release Year Range:', 1920, 2024, (2020, 2024))

# 2. Genre (Mandatory)
genres = ["Action", "Comedy", "Drama", "Fantasy", "Horror", "Romance", "Sci-Fi", "Thriller"]  # You can modify this list based on your preference
selected_genres = st.multiselect('Select Genre(s):', genres)

# 3. IMDb Rating (Mandatory)
rating_range = st.slider('Select IMDb Rating Range:', 7.0, 10.0, (7.0, 10.0))

# 4. Star (Optional)
selected_stars = st.text_input('Enter a Star Name (optional):')

# Debugging: Show what the user selected
st.write(f"Selected Genres: {selected_genres}")
st.write(f"Selected Year Range: {year_range}")
st.write(f"Selected IMDb Rating Range: {rating_range}")
st.write(f"Selected Star: {selected_stars}")

# Collecting movie data from API
top_movies = []
for genre in selected_genres:
    for year in range(year_range[0], year_range[1] + 1):
        # Using the genre as the title search parameter (as an example)
        movie_data = fetch_movie_data(genre, year, api_key)
        st.write(f"API Response for {genre} ({year}): {movie_data}")  # Debugging: Print the API response
        
        if movie_data and 'imdbRating' in movie_data and float(movie_data['imdbRating']) >= rating_range[0]:
            # Check if the selected star is in the movie
            if selected_stars:
                if selected_stars.lower() in movie_data['Actors'].lower():
                    top_movies.append(movie_data)
            else:
                top_movies.append(movie_data)
            if len(top_movies) >= 3:
                break
    if len(top_movies) >= 3:
        break

# Display the results
if top_movies:
    st.write(f"### Top {len(top_movies)} Movies Matching Your Criteria")
    for movie in top_movies:
        st.subheader(f"{movie['Title']} ({movie['Year']})")
        st.image(movie['Poster'], width=150)
        st.write(f"**IMDb Rating:** {movie['imdbRating']}")
        st.write(f"**Genre:** {movie['Genre']}")
        st.write(f"**Director:** {movie['Director']}")
        st.write(f"**Stars:** {movie['Actors']}")
        youtube_search_url = f"https://www.youtube.com/results?search_query={movie['Title']}+trailer"
        st.write(f"[Watch Trailer on YouTube]({youtube_search_url})")
        st.write("---")
else:
    st.write("No movies found matching your criteria.")
