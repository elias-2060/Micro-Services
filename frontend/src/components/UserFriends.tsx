import React, { useEffect, useState } from 'react';
import { fetchFriends, addFriend } from '../api/userApi';
import { useNavigate } from 'react-router-dom';
import '../styles/UserFriends.css';

const Users: React.FC = () => {
  const [friends, setFriends] = useState<{ id: number; username: string }[]>([]);
  const [friendId, setFriendId] = useState('');
  const [message, setMessage] = useState('');
  const [messageType, setMessageType] = useState<'success' | 'error' | ''>('');
  const navigate = useNavigate();

  const storedUser = localStorage.getItem('user');
  const loggedInUser = storedUser ? JSON.parse(storedUser) : null;

  useEffect(() => {
    if (loggedInUser?.id) {
      fetchFriends(loggedInUser.id)
        .then((res) => setFriends(res.data))
        .catch(() => {
          setMessage('Failed to fetch friends');
          setMessageType('error');
        });
    } else {
      setMessage('You are not logged in.');
      setMessageType('error');
    }
  }, []);

  const handleAddFriend = async () => {
    setMessage('');
    setMessageType('');

    if (!friendId) {
      setMessage('Please enter a friend ID');
      setMessageType('error');
      return;
    }

    try {
      const response = await addFriend(loggedInUser.id, parseInt(friendId));
      setMessage(response.data.message);
      setMessageType('success');
      setFriendId('');
      const updated = await fetchFriends(loggedInUser.id);
      setFriends(updated.data);
    } catch (error: any) {
      if (error.response?.status === 404) {
        setMessage('Friend ID not found');
      } else if (error.response?.status === 400) {
        setMessage('Cannot add yourself as a friend');
      } else if (error.response?.status === 409) {
        setMessage('You are already friends');
      } else {
        setMessage('An error occurred while adding the friend');
      }
      setMessageType('error');
    }
  };

  return (
    <div className="users-container">
      <h1>Your Friends</h1>
      {message && <div className={`message ${messageType}`}>{message}</div>}

      {friends.length === 0 ? (
        <p className="no-friends">You have no friends yet.</p>
      ) : (
        <div className="friends-list">
          {friends.map((friend) => (
            <div key={friend.id} className="friend-card">
              <strong>{friend.username}</strong> (ID: {friend.id})
              <button
                className="see-ratings-button"
                onClick={() => navigate(`/friend-ratings/${friend.id}`)}
              >
                See friend's ratings
              </button>
            </div>
          ))}
        </div>
      )}

      <div className="add-friend-form">
        <input
          type="number"
          value={friendId}
          onChange={(e) => setFriendId(e.target.value)}
          placeholder="Enter friend ID"
        />
        <button onClick={handleAddFriend}>Add Friend</button>
      </div>
    </div>
  );
};

export default Users;
