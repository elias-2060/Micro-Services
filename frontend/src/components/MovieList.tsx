import React, { useEffect, useState } from 'react';
import { fetchMovies } from '../api/movieApi';
import { addToWatchHistory, fetchWatchHistory } from '../api/watchApi';
import '../styles/MovieList.css';

interface Movie {
  ID: number;
  "Movie Name": string;
  Rating: number;
  Runtime: string;
  Genre: string;
  Metascore: number;
  Plot: string;
}

const moviesPerPage = 20;

const MovieList: React.FC = () => {
  const [movies, setMovies] = useState<Movie[]>([]);
  const [error, setError] = useState<string | null>(null);
  const [currentPage, setCurrentPage] = useState(1);
  const [watchedIds, setWatchedIds] = useState<number[]>([]);

  const storedUser = localStorage.getItem('user');
  const loggedInUser = storedUser ? JSON.parse(storedUser) : null;

  useEffect(() => {
    const offset = (currentPage - 1) * moviesPerPage;

    fetchMovies(offset, moviesPerPage)
      .then((res) => {
        let parsedData;

        if (typeof res === "string") {
          parsedData = JSON.parse(res);
        } else if (typeof res.data === "string") {
          parsedData = JSON.parse(res.data);
        } else {
          parsedData = res.data;
        }

        if (!Array.isArray(parsedData)) {
          throw new Error("Response is not an array");
        }

        setMovies(parsedData);
        setError(null);
      })
      .catch(() => setError("Failed to fetch movies"));
  }, [currentPage]);

  useEffect(() => {
    if (!loggedInUser?.id) return;
    fetchWatchHistory(loggedInUser.id)
      .then((res) => {
        const ids = res.data.map((item: any) => item.movie_id);
        setWatchedIds(ids);
      })
      .catch(() => setWatchedIds([]));
  }, [loggedInUser]);

  const handleAddToWatchlist = (movieId: number) => {
    if (!loggedInUser?.id) return;
    if (watchedIds.includes(movieId)) return;

    addToWatchHistory(loggedInUser.id, movieId)
      .then(() => setWatchedIds((prev) => [...prev, movieId]))
      .catch((err) => console.error('Failed to add to watch history:', err));
  };

  const handlePrevious = () => setCurrentPage((p) => Math.max(p - 1, 1));
  const handleNext = () => setCurrentPage((p) => p + 1);

  return (
    <div className="gallery-container">
      <h1 className="gallery-title">Movies</h1>
      {error && <p className="gallery-error">{error}</p>}

      <ul className="gallery-grid">
        {movies.map((movie) => (
          <li key={movie.ID} className="gallery-card">
            <h2 className="card-title">{movie["Movie Name"]}</h2>
            <p className="card-runtime">{movie.Runtime}</p>
            <div className="card-details">
              {movie.Genre.split(',').map((g, index) => (
                <span key={index} className="genre-badge">{g.trim()}</span>
              ))}
            </div>
            <p className="card-rating">
              <span className="rating-score">Rating: {movie.Rating}</span>
              <span className="metascore">Metascore: {movie.Metascore}</span>
            </p>
            <p className="card-plot">{movie.Plot}</p>
            <button
              className="watch-button"
              onClick={() => handleAddToWatchlist(movie.ID)}
              disabled={watchedIds.includes(movie.ID)}
            >
              {watchedIds.includes(movie.ID) ? 'Watched' : 'Add to Watchlist'}
            </button>
          </li>
        ))}
      </ul>

      <div className="pagination">
        <button onClick={handlePrevious} disabled={currentPage === 1}>
          Previous
        </button>
        <span>Page {currentPage}</span>
        <button onClick={handleNext}>Next</button>
      </div>
    </div>
  );
};

export default MovieList;
