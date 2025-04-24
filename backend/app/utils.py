import pandas as pd
import pickle
from fuzzywuzzy import process

# Load Data & Models
movies_clean = pd.read_pickle('data/df.pkl')

with open('data/tfidf_vectorizer.pkl', 'rb') as f:
    tfidf = pickle.load(f)
    
with open('data/cosine_similarity.pkl', 'rb') as f:
    cosine_sim = pickle.load(f)

# Title-Based Recommendation Function
def recommend_by_title(user_input):
    """
    Recommend movies based on title similarity using fuzzy matching.
    """
    titles = movies_clean['title'].tolist()
    match, score = process.extractOne(user_input, titles)
    
    if score < 80:
        return None  # Return None if no good match is found
    
    idx = movies_clean[movies_clean['title'] == match].index[0]
    sim_scores = sorted(list(enumerate(cosine_sim[idx])), key=lambda x: x[1], reverse=True)[1:6]
    
    return movies_clean.iloc[[i[0] for i in sim_scores]][['title', 'genre', 'release_year']]

# Filter-Based Recommendation Function
def recommend_by_filters(emotion=None, genre=None, social_context=None, release_year=None):
    """
    Recommend movies based on emotion, genre, social context, and release year.
    """
    filtered = movies_clean.copy()

    if genre:
        filtered = filtered[filtered['genre'].str.contains(genre, case=False, na=False)]
    if release_year:
        filtered = filtered[filtered['release_year'] == release_year]

    # You can add more filtering logic for emotion and social context

    return filtered[['title', 'genre', 'release_year']].head(5)  # Return top 5 recommendations
