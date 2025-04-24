import React from "react";

const MovieCard = ({ title, poster, genre, rating }) => {
  const defaultPoster = "https://via.placeholder.com/300x450?text=No+Image";
  const validPoster = poster ? poster : defaultPoster;

  return (
    <div className="bg-gray-800 text-white rounded-xl overflow-hidden shadow-lg w-64 transition-transform transform hover:scale-105">
      <img
        className="w-full h-96 object-cover"
        src={validPoster}
        alt={title}
        onError={(e) => (e.target.src = defaultPoster)}
      />
      <div className="p-4">
        <h2 className="text-xl font-semibold">{title}</h2>
        {genre && <p className="text-sm text-gray-400 mt-1">Genre: {genre}</p>}
        {rating && (
          <p className="text-sm text-yellow-400 mt-1">⭐ {rating} / 10</p>
        )}
      </div>
    </div>
  );
};

export default MovieCard;
