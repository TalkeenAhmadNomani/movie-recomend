import React, { useState } from "react";
import axios from "axios";
import MovieCard from "./MovieCard";

const MovieRecommendation = () => {
  const [movie, setMovie] = useState("");
  const [titleRecommendations, setTitleRecommendations] = useState([]);
  const [filteredRecommendations, setFilteredRecommendations] = useState([]);
  const [error, setError] = useState("");

  // Filter states
  const [emotion, setEmotion] = useState("");
  const [genre, setGenre] = useState("");
  const [socialContext, setSocialContext] = useState("");
  const [releaseYear, setReleaseYear] = useState("");

  // Fetch recommendations by movie title
  const fetchRecommendations = async () => {
    setError("");
    try {
      const response = await axios.post("http://127.0.0.1:5000/recommend", {
        movie_title: movie,
      });
      setTitleRecommendations(response.data.results || []);
    } catch (error) {
      console.error("Error fetching recommendations", error);
      setError("Failed to fetch recommendations. Try again later.");
    }
  };

  // Fetch recommendations by filters
  const fetchFilterRecommendations = async () => {
    setError("");
    try {
      const response = await axios.post(
        "http://127.0.0.1:5000/recommend_by_filters",
        {
          emotion,
          genre,
          social_context: socialContext,
          release_year: releaseYear,
        }
      );
      setFilteredRecommendations(response.data.results || []);
    } catch (error) {
      console.error("Error fetching filtered recommendations", error);
      setError("Failed to fetch filtered recommendations. Try again later.");
    }
  };

  return (
    <div className="p-4 flex flex-col items-center min-h-screen bg-gray-900 text-white">
      <h1 className="text-3xl font-bold mb-4 text-center">
        Movie Recommendation System
      </h1>

      {/* Search by Movie Title */}
      <div className="flex flex-col sm:flex-row gap-2 w-full max-w-md">
        <input
          type="text"
          value={movie}
          onChange={(e) => setMovie(e.target.value)}
          placeholder="Enter a movie name"
          className="p-2 border rounded-md text-white bg-black w-full focus:outline-none"
        />
        <button
          onClick={fetchRecommendations}
          className="bg-blue-500 px-4 py-2 rounded-md text-white hover:bg-blue-700 transition"
        >
          Get Recommendations
        </button>
      </div>

      {/* Filters Section */}
      <div className="mt-6 w-full max-w-md flex flex-col items-center">
        <h2 className="text-xl mb-2">Filter Recommendations</h2>
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-4 w-full">
          {[
            {
              label: "Emotion",
              state: emotion,
              setState: setEmotion,
              options: ["happy", "sad", "exciting"],
            },
            {
              label: "Genre",
              state: genre,
              setState: setGenre,
              options: ["action", "drama", "comedy"],
            },
            {
              label: "Context",
              state: socialContext,
              setState: setSocialContext,
              options: ["family", "friends", "solo"],
            },
            {
              label: "Year",
              state: releaseYear,
              setState: setReleaseYear,
              options: ["classic", "recent"], // Updated to match backend
            },
          ].map(({ label, state, setState, options }, index) => (
            <select
              key={index}
              value={state}
              onChange={(e) => setState(e.target.value)}
              className="p-2 border rounded-md text-white bg-black w-full"
            >
              <option value="">Select {label}</option>
              {options.map((option, idx) => (
                <option key={idx} value={option}>
                  {option.charAt(0).toUpperCase() + option.slice(1)}
                </option>
              ))}
            </select>
          ))}
        </div>
        <button
          onClick={fetchFilterRecommendations}
          className="bg-green-500 px-4 py-2 rounded-md text-white hover:bg-green-700 transition mt-4"
        >
          Get Filtered Recommendations
        </button>
      </div>

      {error && <p className="text-red-500 mt-4">{error}</p>}

      {/* Display Recommendations */}
      <div className="mt-6 w-full max-w-6xl">
        {titleRecommendations.length > 0 && (
          <>
            <h2 className="text-xl font-semibold mb-2">
              Recommendations for "{movie}"
            </h2>
            <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 gap-6">
              {titleRecommendations.map((rec, index) => (
                <MovieCard
                  key={index}
                  title={rec.title}
                  genre={rec.genres}
                  rating={rec.rating}
                  poster={rec.poster_url}
                />
              ))}
            </div>
          </>
        )}

        {filteredRecommendations.length > 0 && (
          <>
            <h2 className="text-xl font-semibold mt-6 mb-2">
              Filtered Recommendations
            </h2>
            <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 gap-6">
              {filteredRecommendations.map((rec, index) => (
                <MovieCard
                  key={index}
                  title={rec.title}
                  genre={rec.genres}
                  rating={rec.rating}
                  poster={rec.poster_url}
                />
              ))}
            </div>
          </>
        )}
      </div>
    </div>
  );
};

export default MovieRecommendation;
