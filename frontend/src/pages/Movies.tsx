import React from 'react';
import Navbar from '../components/Navbar';
import MovieList from '../components/MovieList';
import './Movies.css';

const Movies: React.FC = () => {
  return (
    <>
      <Navbar />
      <div className="movies-page">
        <MovieList />
      </div>
    </>
  );
};

export default Movies;
