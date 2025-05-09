import axios from 'axios';

const API_BASE = 'http://localhost:5004';

export const fetchTopRatedMovies = (userId: number) => {
  return axios.get(`${API_BASE}/recommend/top/${userId}/`);
};

export const fetchFriendRecommendations = (userId: number) => {
  return axios.get(`${API_BASE}/recommend/friends/${userId}/`);
};
