import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import '../styles/Navbar.css';

const Navbar: React.FC = () => {
  const location = useLocation();

  return (
    <nav className="navbar">
      <Link to="/home" className="navbar-title-link">
        <h1 className="navbar-title">🎬 NextFilm</h1>
      </Link>
      <ul className="navbar-links">
        <li>
          <Link to="/movies" className={location.pathname === '/movies' ? 'active' : ''}>Movies</Link>
        </li>
        <li>
          <Link to="/newsfeed" className={location.pathname === '/newsfeed' ? 'active' : ''}>Newsfeed</Link>
        </li>
        <li>
          <Link to="/friends" className={location.pathname === '/friends' ? 'active' : ''}>Friends</Link>
        </li>
        <li>
          <Link to="/watched" className={location.pathname === '/watched' ? 'active' : ''}>Latest Watched</Link>
        </li>
        <li>
          <Link to="/recommendations" className={location.pathname === '/recommendations' ? 'active' : ''}>Recommendations</Link>
        </li>
      </ul>
    </nav>
  );
};

export default Navbar;
