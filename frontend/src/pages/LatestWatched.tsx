import React, { useEffect, useState } from 'react';
import Navbar from '../components/Navbar';
import { fetchWatchHistory } from '../api/WatchApi';
import { fetchMovieById } from '../api/MovieApi';
import './LatestWatched.css';

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

const LatestWatched: React.FC = () => {
  const [movies, setMovies] = useState<Movie[]>([]);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const loadWatchedMovies = async () => {
      const storedUser = localStorage.getItem('user');
      const loggedInUser = storedUser ? JSON.parse(storedUser) : null;

      if (!loggedInUser || !loggedInUser.id) {
        setError('User not logged in');
        setLoading(false);
        return;
      }

      try {
        const res = await fetchWatchHistory(loggedInUser.id);
        const watchData: WatchedMovie[] = res.data;

        if (!watchData.length) {
          setError('You haven’t watched any movies yet.');
          setLoading(false);
          return;
        }

        const detailedMovies = await Promise.all(
          watchData.map(async ({ movie_id }) => {
            try {
              const response = await fetchMovieById(movie_id);
              const data = typeof response.data === 'string'
                ? JSON.parse(response.data)
                : response.data;

              if (Array.isArray(data)) {
                return data[0]; // <<== FIX HERE
              }

              return data;
            } catch (err) {
              console.error(`Failed to fetch movie ${movie_id}`, err);
              return null;
            }
          })
        );

        setMovies(detailedMovies.filter(Boolean) as Movie[]);
        setLoading(false);
      } catch (err) {
        console.error('Failed to fetch watch history', err);
        setError('Failed to load watch history');
        setLoading(false);
      }
    };

    loadWatchedMovies();
  }, []);

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
            {movies.map((movie) => (
              <li key={movie.ID} className="movie-card">
                <h2>{movie["Movie Name"]}</h2>
                <p className="runtime">{movie.Runtime}</p>

                <div className="details">
                  {movie.Genre?.split(',').map((g, index) => (
                    <span key={index} className="genre-badge">{g.trim()}</span>
                  ))}
                </div>

                <p className="rating">
                  <span className="rating-score">Rating: {movie.Rating}</span>
                  <span className="metascore">Metascore: {movie.Metascore}</span>
                </p>

                <p className="plot">{movie.Plot}</p>
              </li>
            ))}
          </ul>
        )}
      </div>
    </>
  );
};

export default LatestWatched;
