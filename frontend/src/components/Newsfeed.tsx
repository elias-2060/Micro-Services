import React, { useEffect, useState } from 'react';
import Navbar from '../components/Navbar';
import { fetchNewsfeed } from '../api/newsfeedApi';
import { fetchMovieById } from '../api/movieApi';
import '../styles/NewsfeedComp.css';

interface NewsItem {
  friend_id: number;
  friend_username: string;
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

const Newsfeed: React.FC = () => {
  const [news, setNews] = useState<NewsItem[]>([]);
  const [movies, setMovies] = useState<{ [movieId: number]: Movie }>({});
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const storedUser = localStorage.getItem('user');
    const loggedInUser = storedUser ? JSON.parse(storedUser) : null;
    const userId = loggedInUser?.id;

    if (!userId) {
      setError("User not logged in");
      return;
    }

    fetchNewsfeed(userId)
      .then(async (res) => {
        const items: NewsItem[] = res.data.newsfeed;
        setNews(items);

        const movieIdsArray = items.map((item) => item.movie_id);
        const uniqueMovieIds = Array.from(new Set(movieIdsArray));

        const movieDetails: { [movieId: number]: Movie } = {};

        for (let i = 0; i < uniqueMovieIds.length; i++) {
          const movieId = uniqueMovieIds[i];
          try {
            const res = await fetchMovieById(movieId);
            const data = typeof res.data === 'string' ? JSON.parse(res.data) : res.data;
            const movie = Array.isArray(data) ? data[0] : data;
            movieDetails[movieId] = movie;
          } catch {
            continue;
          }
        }

        setMovies(movieDetails);
      })
      .catch(() => setError('Failed to load newsfeed'));
  }, []);

  return (
    <>
      <div className="newsfeed-wrapper">
        <h1 className="newsfeed-header">Newsfeed</h1>
        {error && <p className="newsfeed-error">{error}</p>}

        <div className="newsfeed-card-container">
          {news.map((item: NewsItem, index: number) => {
            const movie = movies[item.movie_id];
            if (!movie) return null;

            return (
              <div key={index} className="newsfeed-card">
                <h2 className="newsfeed-movie-title">{movie["Movie Name"]}</h2>
                <p className="newsfeed-runtime">{movie.Runtime}</p>
                <div className="newsfeed-genres">
                  {movie.Genre?.split(',').map((genre, i) => (
                    <span key={i} className="newsfeed-genre-badge">{genre.trim()}</span>
                  ))}
                </div>
                <p className="newsfeed-ratings">
                  <span className="newsfeed-rating">Rating: {movie.Rating}</span>
                  <span className="newsfeed-metascore">Metascore: {movie.Metascore}</span>
                </p>
                <p className="newsfeed-plot">{movie.Plot}</p>
                <p className="newsfeed-meta-info">
                  <strong>{item.friend_username}</strong> watched this on{' '}
                  {new Date(item.timestamp).toLocaleString()}
                </p>
              </div>
            );
          })}
        </div>
      </div>
    </>
  );
};

export default Newsfeed;
