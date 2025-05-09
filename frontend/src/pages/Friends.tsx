import React from 'react';
import Navbar from '../components/Navbar';
import UserFriends from '../components/UserFriends';
import '../styles/Friends.css';

const Friends: React.FC = () => {
  return (
    <>
      <Navbar />
      <div className="users-page">
        <UserFriends />
      </div>
    </>
  );
};

export default Friends;
