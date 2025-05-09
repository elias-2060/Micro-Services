import React, { useEffect, useState } from 'react';
import Navbar from '../components/Navbar';
import { fetchTopRatedMovies, fetchFriendRecommendations } from '../api/recommendationApi';
import { fetchMovieById } from '../api/movieApi';
import '../styles/RecommendationPage.css';

interface Movie {
  ID: number;
  'Movie Name': string;
  Genre: string;
  Rating: number;
  Runtime: string;
  Metascore: number;
  Plot: string;
}

const RecommendationPage: React.FC = () => {
  const [topRated, setTopRated] = useState<Movie[]>([]);
  const [friendBased, setFriendBased] = useState<Movie[]>([]);
  const [error, setError] = useState('');

  const storedUser = localStorage.getItem('user');
  const loggedInUser = storedUser ? JSON.parse(storedUser) : null;

  useEffect(() => {
    const loadRecommendations = async () => {
      if (!loggedInUser?.id) {
        setError('User not logged in');
        return;
      }

      try {
        const [topRes, friendRes] = await Promise.all([
          fetchTopRatedMovies(loggedInUser.id),
          fetchFriendRecommendations(loggedInUser.id),
        ]);

        const topMoviePromises = topRes.data.map((item: any) => fetchMovieById(item.movie_id));
        const friendMoviePromises = friendRes.data.recommendations.map((mid: number) => fetchMovieById(mid));

        const topMovieDetails = await Promise.all(topMoviePromises);
        const friendMovieDetails = await Promise.all(friendMoviePromises);

        const parseMovie = (res: any) =>
          typeof res.data === 'string' ? JSON.parse(res.data)[0] : res.data[0];

        setTopRated(topMovieDetails.map(parseMovie));
        setFriendBased(friendMovieDetails.map(parseMovie));
      } catch (err) {
        setError('Failed to load recommendations');
      }
    };

    loadRecommendations();
  }, []);

  const renderMovieCards = (movies: Movie[]) => (
    <ul className="recommendation-slider">
      {movies.map((movie) => (
        <li key={movie.ID} className="recommendation-card">
          <h2>{movie['Movie Name']}</h2>
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
        </li>
      ))}
    </ul>
  );

  return (
    <>
      <Navbar />
      <div className="recommendation-page">
        <h1 className="main-title">Recommended for You</h1>
        {error && <p className="error">{error}</p>}

        <h3 className="section-title">Top Rated Movies</h3>
        {renderMovieCards(topRated)}

        <h3 className="section-title">Because Your Friends Watched</h3>
        {renderMovieCards(friendBased)}
      </div>
    </>
  );
};

export default RecommendationPage;
