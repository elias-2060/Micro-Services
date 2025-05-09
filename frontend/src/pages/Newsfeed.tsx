import React from 'react';
import Navbar from '../components/Navbar';
import Newsfeed from '../components/Newsfeed';
import '../styles/Newsfeed.css';

const NewsfeedPage: React.FC = () => {
  return (
    <>
      <Navbar />
      <div className="newsfeed-page">
        <Newsfeed />
      </div>
    </>
  );
};

export default NewsfeedPage;
