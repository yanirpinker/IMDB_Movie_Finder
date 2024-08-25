import streamlit as st
import pandas as pd

# Load the dataset
df = pd.read_csv('imdb_top_1000.csv')

# Ensure correct data types
df['Released_Year'] = pd.to_numeric(df['Released_Year'], errors='coerce')
df['IMDB_Rating'] = pd.to_numeric(df['IMDB_Rating'], errors='coerce')

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

# Streamlit UI components with enhanced style
st.title("🎬 Find Your Next Movie")

st.subheader("Specify Your Preferences")

# 1. Release Year (Mandatory)
year_range = st.slider('Select Release Year Range:', 1920, 2024, (2020, 2024))

# 2. Genre (Mandatory)
genres = sorted(set([g.strip() for sublist in df['Genre'].str.split(',').tolist() for g in sublist]))
selected_genres = st.multiselect('Select Genre(s):', genres)

# 3. IMDb Rating (Mandatory)
rating_range = st.slider('Select IMDb Rating Range:', 7.0, 10.0, (7.0, 10.0))

# 4. Star (Optional)
stars = sorted(df['Star1'].unique())
selected_stars = st.multiselect('Select Star(s) (optional):', stars)

# Filter the dataset based on user inputs
filtered_df = df[(df['Released_Year'] >= year_range[0]) & (df['Released_Year'] <= year_range[1])]
filtered_df = filtered_df[filtered_df['IMDB_Rating'].between(rating_range[0], rating_range[1])]

if selected_genres:
    filtered_df = filtered_df[filtered_df['Genre'].apply(lambda x: any(g in x for g in selected_genres))]

if selected_stars:
    filtered_df = filtered_df[filtered_df['Star1'].isin(selected_stars) | 
                              filtered_df['Star2'].isin(selected_stars) | 
                              filtered_df['Star3'].isin(selected_stars) | 
                              filtered_df['Star4'].isin(selected_stars)]

# Ensure the column exists and then get top 3 movies by rating
if 'IMDB_Rating' in filtered_df.columns and not filtered_df.empty:
    top_movies = filtered_df.nlargest(3, 'IMDB_Rating')
else:
    top_movies = pd.DataFrame()  # Empty DataFrame if no movies match the criteria

# Display the results
if not top_movies.empty:
    st.write(f"### Top {len(top_movies)} Movies Matching Your Criteria")
    for _, row in top_movies.iterrows():
        st.subheader(f"{row['Series_Title']} ({row['Released_Year']})")
        st.image(row['Poster_Link'], width=150)
        st.write(f"**IMDb Rating:** {row['IMDB_Rating']}")
        st.write(f"**Genre:** {row['Genre']}")
        st.write(f"**Director:** {row['Director']}")
        st.write(f"**Stars:** {row['Star1']}, {row['Star2']}, {row['Star3']}, {row['Star4']}")
        st.write("---")
else:
    st.write("No movies found matching your criteria.")
