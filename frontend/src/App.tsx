import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Movies from './pages/Movies';
import NewsfeedPage from './pages/Newsfeed';
import Friends from './pages/Friends';
import RegisterPage from './pages/Register';
import LoginPage from './pages/Login';
import Home from './pages/Home';
import LatestWatched from './pages/LatestWatched';

const App: React.FC = () => {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<RegisterPage />} />
        <Route path="/home" element={<Home />} />
        <Route path="/login" element={<LoginPage />} />
        <Route path="/movies" element={<Movies />} />
        <Route path="/newsfeed" element={<NewsfeedPage />} />
        <Route path="/friends" element={<Friends />} />
        <Route path="/watched" element={<LatestWatched />} />
      </Routes>
    </Router>
  );
};

export default App;
