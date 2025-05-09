import React, { useEffect, useState } from 'react';
import Navbar from '../components/Navbar';
import { fetchWatchHistory } from '../api/watchApi';
import { fetchMovieById } from '../api/movieApi';
import { rateMovie, fetchUserRatings } from '../api/ratingApi';
import '../styles/LatestWatched.css';

interface WatchedMovie {
  movie_id: number;
  timestamp: string;
}

interface Movie {
  ID: number;
  "Movie Name": string;
  Genre: string;
  Rating: number;
  Runtime: string;
  Metascore: number;
  Plot: string;
}

interface Rating {
  movie_id: number;
  score: number;
  agrees: number;
  disagrees: number;
}

const LatestWatched: React.FC = () => {
  const [movies, setMovies] = useState<Movie[]>([]);
  const [ratings, setRatings] = useState<Rating[]>([]);
  const [ratingInputs, setRatingInputs] = useState<{ [movieId: number]: number }>({});
  const [ratingStatus, setRatingStatus] = useState<{ [movieId: number]: string }>({});
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);

  const storedUser = localStorage.getItem('user');
  const loggedInUser = storedUser ? JSON.parse(storedUser) : null;

  useEffect(() => {
    const loadData = async () => {
      if (!loggedInUser?.id) {
        setError('User not logged in');
        setLoading(false);
        return;
      }

      try {
        const [watchRes, ratingsRes] = await Promise.all([
          fetchWatchHistory(loggedInUser.id),
          fetchUserRatings(loggedInUser.id),
        ]);

        const watchedMovies: WatchedMovie[] = watchRes.data;
        setRatings(ratingsRes.data);

        const detailedMovies = await Promise.all(
          watchedMovies.map(async ({ movie_id }) => {
            try {
              const res = await fetchMovieById(movie_id);
              const data = typeof res.data === 'string' ? JSON.parse(res.data) : res.data;
              return Array.isArray(data) ? data[0] : data;
            } catch {
              return null;
            }
          })
        );

        setMovies(detailedMovies.filter(Boolean) as Movie[]);
      } catch {
        setError('Failed to load data');
      } finally {
        setLoading(false);
      }
    };

    loadData();
  }, []);

  const getUserRating = (movieId: number): Rating | undefined =>
    ratings.find((r) => r.movie_id === movieId);

  const handleScoreChange = (movieId: number, value: number) => {
    setRatingInputs((prev) => ({ ...prev, [movieId]: value }));
  };

  const handleRateMovie = async (movieId: number) => {
    if (!loggedInUser?.id || !ratingInputs[movieId]) {
      setRatingStatus((prev) => ({ ...prev, [movieId]: 'Invalid input or user not logged in.' }));
      return;
    }

    try {
      await rateMovie(loggedInUser.id, movieId, ratingInputs[movieId]);
      const updatedRatings = await fetchUserRatings(loggedInUser.id);
      setRatings(updatedRatings.data);
      setRatingStatus((prev) => ({ ...prev, [movieId]: 'Rating submitted!' }));
    } catch {
      setRatingStatus((prev) => ({ ...prev, [movieId]: 'Failed to submit rating.' }));
    }
  };

  return (
    <>
      <Navbar />
      <div className="movie-list-container">
        <h1 className="title">Watched Movies</h1>

        {loading ? (
          <p className="loading">Loading...</p>
        ) : error ? (
          <p className="error">{error}</p>
        ) : (
          <ul className="movie-grid">
            {movies.map((movie) => {
              const userRating = getUserRating(movie.ID);
              return (
                <li key={movie.ID} className="movie-card">
                  <h2>{movie["Movie Name"]}</h2>
                  <p className="runtime">{movie.Runtime}</p>

                  <div className="details">
                    {movie.Genre?.split(',').map((g, idx) => (
                      <span key={idx} className="genre-badge">{g.trim()}</span>
                    ))}
                  </div>

                  <p className="rating">
                    <span className="rating-score">Rating: {movie.Rating}</span>
                    <span className="metascore">Metascore: {movie.Metascore}</span>
                  </p>

                  <p className="plot">{movie.Plot}</p>

                  {userRating ? (
                    <>
                      <p className="user-rating">You rated this: {userRating.score} / 10</p>
                      <div className="reaction-counts centered-reactions">
                        <span className="agree-count">👍 {userRating.agrees ?? 0}</span>
                        <span className="disagree-count">👎 {userRating.disagrees ?? 0}</span>
                      </div>
                    </>
                  ) : (
                    <div className="rating-form">
                      <input
                        type="number"
                        min="1"
                        max="10"
                        placeholder="Rate 1–10"
                        value={ratingInputs[movie.ID] || ''}
                        onChange={(e) => handleScoreChange(movie.ID, parseInt(e.target.value))}
                      />
                      <button onClick={() => handleRateMovie(movie.ID)}>Submit Rating</button>
                      {ratingStatus[movie.ID] && <p className="rating-message">{ratingStatus[movie.ID]}</p>}
                    </div>
                  )}
                </li>
              );
            })}
          </ul>
        )}
      </div>
    </>
  );
};

export default LatestWatched;
