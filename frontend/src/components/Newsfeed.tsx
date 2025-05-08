import React, { useEffect, useState } from 'react';
import { fetchNewsfeed } from '../api/newsfeedApi';
import './Newsfeed.css'; // Import the CSS file

interface NewsItem {
  friend_id: number;
  friend_username: string;
  movie_id: number;
  timestamp: string;
}

const Newsfeed: React.FC = () => {
  const [news, setNews] = useState<NewsItem[]>([]);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const userId = 1;
    fetchNewsfeed(userId)
      .then((res) => setNews(res.data.newsfeed))
      .catch(() => setError("Failed to load newsfeed"));
  }, []);

  return (
    <div className="newsfeed-container">
      <h1 className="newsfeed-title">Newsfeed</h1>
      {error && <p className="error-message">{error}</p>}
      <ul className="newsfeed-list">
        {news.map((item, idx) => (
          <li key={idx} className="newsfeed-item">
            <p><strong>{item.friend_username}</strong> watched movie ID {item.movie_id}</p>
            <p className="newsfeed-meta">{new Date(item.timestamp).toLocaleString()}</p>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default Newsfeed;
