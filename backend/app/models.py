from flask import Blueprint, request, jsonify
import pandas as pd
import pickle
from fuzzywuzzy import process

api_bp = Blueprint("api", __name__)

# Load Data & Models
movies_clean = pd.read_pickle('data/df.pkl')

with open('data/tfidf_vectorizer.pkl', 'rb') as f:
    tfidf = pickle.load(f)
with open('data/cosine_similarity.pkl', 'rb') as f:
    cosine_sim = pickle.load(f)

# Title-Based Recommendation Function
def recommend_by_title(user_input):
    titles = movies_clean['title'].tolist()
    match, score = process.extractOne(user_input, titles)
    
    if score < 80:
        return []

    idx = movies_clean[movies_clean['title'] == match].index[0]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)[1:6]

    recommended_movies = movies_clean.iloc[[i[0] for i in sim_scores]]

    return recommended_movies[['title', 'genre', 'rating']].to_dict(orient='records')  # Convert to JSON

@api_bp.route("/recommend", methods=["POST"])
def recommend_movies():
    try:
        data = request.get_json()
        movie_name = data.get("movie")

        if not movie_name:
            return jsonify({"error": "Movie name is required"}), 400

        recommendations = recommend_by_title(movie_name)

        if not recommendations:
            return jsonify({"error": "No similar movies found"}), 404

        return jsonify({"recommendations": recommendations})

    except Exception as e:
        return jsonify({"error": str(e)}), 500
