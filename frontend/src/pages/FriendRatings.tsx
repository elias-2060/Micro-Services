import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import { fetchUserRatings, reactToRating, fetchUserReactions } from '../api/ratingApi';
import { fetchMovieById } from '../api/movieApi';
import Navbar from '../components/Navbar';
import '../styles/FriendRatings.css';

interface Rating {
  movie_id: number;
  score: number;
  agrees: number;
  disagrees: number;
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

interface Reaction {
  user_id: number;
  movie_id: number;
  reactor_id: number;
  reaction_type: 'agree' | 'disagree';
}

const FriendRatings: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const [ratings, setRatings] = useState<Rating[]>([]);
  const [movies, setMovies] = useState<Movie[]>([]);
  const [reactionStatus, setReactionStatus] = useState<{ [movieId: number]: string }>({});
  const [reactedTo, setReactedTo] = useState<Set<string>>(new Set());
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const storedUser = localStorage.getItem('user');
  const loggedInUser = storedUser ? JSON.parse(storedUser) : null;

  useEffect(() => {
    const loadData = async () => {
      if (!id || !loggedInUser?.id) {
        setError('Friend ID or logged-in user not found.');
        setLoading(false);
        return;
      }

      try {
        // Fetch friend's ratings and current user's past reactions
        const [ratingsRes, reactionsRes] = await Promise.all([
          fetchUserRatings(parseInt(id)),
          fetchUserReactions(loggedInUser.id),
        ]);

        setRatings(ratingsRes.data);

        const movieData = await Promise.all(
          ratingsRes.data.map(async (r: Rating) => {
            try {
              const res = await fetchMovieById(r.movie_id);
              const data = typeof res.data === 'string' ? JSON.parse(res.data) : res.data;
              return Array.isArray(data) ? data[0] : data;
            } catch {
              return null;
            }
          })
        );

        const reacted = new Set<string>();
        reactionsRes.data.forEach((r: Reaction) => {
          reacted.add(`${r.user_id}-${r.movie_id}`);
        });
        setReactedTo(reacted);

        setMovies(movieData.filter(Boolean) as Movie[]);
      } catch (err) {
        setError('Failed to fetch data');
      } finally {
        setLoading(false);
      }
    };

    loadData();
  }, [id]);

  const handleReaction = async (movieId: number, type: 'agree' | 'disagree') => {
    if (!loggedInUser?.id || !id || reactedTo.has(`${id}-${movieId}`)) return;

    try {
      await reactToRating(parseInt(id), movieId, loggedInUser.id, type);
      setReactionStatus((prev) => ({
        ...prev,
        [movieId]: `You ${type}d this rating.`,
      }));
      setReactedTo((prev) => new Set(prev).add(`${id}-${movieId}`));
      setRatings((prevRatings) =>
        prevRatings.map((r) =>
          r.movie_id === movieId
            ? {
                ...r,
                agrees: type === 'agree' ? r.agrees + 1 : r.agrees,
                disagrees: type === 'disagree' ? r.disagrees + 1 : r.disagrees,
              }
            : r
        )
      );
    } catch {
      setReactionStatus((prev) => ({
        ...prev,
        [movieId]: `Failed to ${type}.`,
      }));
    }
  };

  return (
    <>
      <Navbar />
      <div className="movie-list-container">
        <h1 className="title">Friend's Rated Movies</h1>

        {loading ? (
          <p className="loading">Loading...</p>
        ) : error ? (
          <p className="error">{error}</p>
        ) : (
          <ul className="movie-grid">
            {movies.map((movie) => {
              const rating = ratings.find((r) => r.movie_id === movie.ID);
              const hasReacted = reactedTo.has(`${id}-${movie.ID}`);

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

                  {rating && (
                    <div className="friend-rating">
                      <p className="score-display">Score: <span className="score-green animate-score">{rating.score}</span></p>
                      <p className="reaction-counts">
                        <span className="agree-count">👍 {rating.agrees}</span>
                        <span className="disagree-count">👎 {rating.disagrees}</span>
                      </p>
                      <div className="reaction-buttons">
                        <button
                          className="agree-btn"
                          disabled={hasReacted}
                          onClick={() => handleReaction(movie.ID, 'agree')}
                        >
                          Agree
                        </button>
                        <button
                          className="disagree-btn"
                          disabled={hasReacted}
                          onClick={() => handleReaction(movie.ID, 'disagree')}
                        >
                          Disagree
                        </button>
                      </div>
                      {reactionStatus[movie.ID] && (
                        <p className="reaction-status">{reactionStatus[movie.ID]}</p>
                      )}
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

export default FriendRatings;
