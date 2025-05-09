import axios from 'axios';

const BASE_URL = 'http://localhost:5002';

// Add a movie to a user's watch history
export const addToWatchHistory = async (userId: number, movieId: number) => {
  return axios.post(`${BASE_URL}/watch/${userId}/${movieId}/`);
};

// Fetch all watched movies for a user
export const fetchWatchHistory = (userId: number) => {
  return axios.get(`${BASE_URL}/watch/${userId}/`);
};
