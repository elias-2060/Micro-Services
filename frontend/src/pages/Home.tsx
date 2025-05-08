import React from 'react';
import Navbar from '../components/Navbar';
import './Home.css';

const Home: React.FC = () => {
  return (
    <>
      <Navbar />
      <div className="home-page">
        <h1>Welcome to NextFilm</h1>
        <p>Explore top-rated movies and see what your friends are watching.</p>
      </div>
    </>
  );
};

export default Home;
