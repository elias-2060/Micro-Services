import React, { useState } from 'react';
import { loginUser } from '../api/userApi';
import './AuthForm.css';
import { Link, useNavigate } from 'react-router-dom';

const LoginPage: React.FC = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const response = await loginUser(username, password);
      const userId = response.data.user_id;

      // Save user info to localStorage
      localStorage.setItem('user', JSON.stringify({ id: response.data.user_id, username }));


      // Navigate to home
      navigate('/home');
    } catch (err: any) {
      setError(err.response?.data?.error || 'Login failed');
    }
  };

  return (
    <div className="login-container">
      <h2>Login</h2>
      <form onSubmit={handleLogin}>
        <input
          type="text"
          placeholder="Username"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          required
        />
        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
        />
        <button type="submit">Login</button>
      </form>
      {error && <div className="error-message">{error}</div>}
      <p>
        Don’t have an account? <Link to="/">Register here</Link>.
      </p>
    </div>
  );
};

export default LoginPage;
