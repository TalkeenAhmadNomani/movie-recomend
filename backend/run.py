from flask import Flask, request, jsonify
import pandas as pd
import pickle
from fuzzywuzzy import process
from flask_cors import CORS
import requests  # Added for TMDB API

app = Flask(__name__)

# Enable CORS explicitly for frontend at localhost:5173
CORS(app, resources={r"/*": {"origins": "http://localhost:5173"}}, supports_credentials=True)

# Load data and models
try:
    movies_clean = pd.read_pickle('data/df.pkl')
    with open('data/tfidf_vectorizer.pkl', 'rb') as f:
        tfidf = pickle.load(f)
    with open('data/cosine_similarity.pkl', 'rb') as f:
        cosine_sim = pickle.load(f)
   
except Exception as e:

    movies_clean, cosine_sim = None, None

# 📌 TMDB API Configuration
TMDB_API_KEY = "9243e5f6f0fdfaf8687d2b5c7364613f"
TMDB_BASE_URL = "https://api.themoviedb.org/3"



def get_movie_poster(movie_id):
    """Fetches the movie poster URL from TMDB API using movie_id."""
    url = f"{TMDB_BASE_URL}/movie/{movie_id}?api_key={TMDB_API_KEY}"
    print(f"Fetching URL: {url}")  # Debugging print

    response = requests.get(url)
    print(f"Response Status Code: {response.status_code}")  # Debugging print

    if response.status_code == 200:
        data = response.json()
        print(f"Response Data: {data}")  # Debugging print

        poster_path = data.get("poster_path")
        if poster_path:
            poster_url = f"https://image.tmdb.org/t/p/w500{poster_path}"
            print(f"Poster URL: {poster_url}")  # Debugging print
            return poster_url
        else:
            print("Poster path not found in response.")
    else:
        print(f"Failed to fetch poster. Status Code: {response.status_code}, Response: {response.text}")

    return None
 # If no poster is found

# 📌 **Title-Based Recommendation**
def recommend_by_title(user_input):
    titles = movies_clean['title'].tolist()
    match, score = process.extractOne(user_input, titles)

 

    if score < 80:
        print("⚠️ No close match found.")
        return []

    idx_list = movies_clean[movies_clean['title'] == match].index.tolist()
    
    if not idx_list:
        print("⚠️ No matching index found.")
        return []

    idx = idx_list[0]

    if idx >= len(cosine_sim):  # Check if index exists in similarity matrix
        print("⚠️ Index out of range in cosine similarity.")
        return []

    sim_scores = sorted(enumerate(cosine_sim[idx]), key=lambda x: x[1], reverse=True)[1:10]
    
    recommended_movies = []
    for i in sim_scores:
        movie_data = movies_clean.iloc[i[0]].to_dict()
        movie_id = movie_data.get("movie_id")  # Fetch movie_id
        poster_url = get_movie_poster(movie_id) if movie_id else None
        movie_data["poster_url"] = poster_url  # Add poster URL
        recommended_movies.append(movie_data)

    return recommended_movies


# 📌 **Filter-Based Recommendation**
def recommend_by_filters(emotion=None, genre=None, social_context=None, release_year=None, limit=5):
    filtered = movies_clean.copy()

    # Apply filters
    if emotion:
        filtered = filtered[filtered['emotion'].str.lower() == emotion.lower()]
    
    if genre:
        filtered = filtered[filtered['genres'].str.contains(genre, case=False, na=False)]
    
    if social_context:
        filtered = filtered[filtered['social_context'].str.contains(social_context, case=False, na=False)]
    
    if release_year:
        if release_year.lower() == 'recent':
            filtered = filtered[filtered['release_year'] >= 2020]
        elif release_year.lower() == 'classic':
            filtered = filtered[filtered['release_year'] < 2000]

    # Fallback to top-rated movies if no results
    if filtered.empty:
        filtered = movies_clean.sort_values(['vote_average', 'release_year'], ascending=[False, False])

    # Calculate a custom score
    filtered['score'] = (
        0.5 * filtered['vote_average'] +
        0.3 * (filtered['release_year'] / 2023) +
        0.4 * filtered['sentiment'].abs()
    )

    # Sort by score and limit results
    results = filtered.sort_values('score', ascending=False).head(limit).to_dict(orient='records')

    # Attach poster URLs
    for movie in results:
        movie_id = movie.get("movie_id")
        if movie_id:
            movie["poster_url"] = get_movie_poster(movie_id)
        else:
            movie["poster_url"] = None

    return results



# 📌 **API Routes**
@app.route('/')
def home():
    return "✅ Flask API is running!"


@app.route('/recommend', methods=['POST'])
def recommend():
    data = request.get_json()
    
    if not data or 'movie_title' not in data:
        print("❌ Invalid request format.")
        return jsonify({'error': 'Invalid JSON data'}), 400

    title = data['movie_title']
    results = recommend_by_title(title)

    if not results:
        print("⚠️ No recommendations found.")

    return jsonify({'results': results}), 200


@app.route('/recommend_by_filters', methods=['POST'])
def recommend_filters():
    data = request.get_json()

    if not data:
        print("❌ Invalid request format.")
        return jsonify({'error': 'Invalid JSON data'}), 400

    emotion = data.get('emotion')
    genre = data.get('genre')
    social_context = data.get('social_context')
    release_year = data.get('release_year')

    results = recommend_by_filters(emotion, genre, social_context, release_year)

    return jsonify({'results': results}), 200


if __name__ == '__main__':
    app.run(debug=True)
