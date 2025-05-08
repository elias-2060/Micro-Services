import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import './Navbar.css';

const Navbar: React.FC = () => {
  const location = useLocation();

  return (
    <nav className="navbar">
      <h1 className="navbar-title">🎬 NextFilm</h1>
      <ul className="navbar-links">
        <li>
          <Link to="/home" className={location.pathname === '/home' ? 'active' : ''}>Home</Link>
        </li>
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
      </ul>
    </nav>
  );
};

export default Navbar;
