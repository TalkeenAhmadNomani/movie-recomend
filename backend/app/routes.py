from flask import Blueprint, request, jsonify
from app.utils import recommend_by_title, recommend_by_filters

api_bp = Blueprint("api", __name__)  # Define Blueprint properly

@api_bp.route("/recommend", methods=["POST"])
def recommend():
    data = request.get_json()
    title = data.get("movie")

    if not title:
        return jsonify({"error": "No movie title provided"}), 400

    results = recommend_by_title(title)

    if results is None:
        return jsonify({"error": "No recommendations found"}), 404

    return jsonify({"recommendations": results.to_dict(orient="records")}), 200
