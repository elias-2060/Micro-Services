import axios from 'axios';

const BASE_URL = 'http://localhost:5003';

export const rateMovie = (userId: number, movieId: number, score: number) => {
  return axios.post(`${BASE_URL}/ratings/${userId}/${movieId}/`, { score });
};

export const fetchUserRatings = (userId: number) => {
  return axios.get(`${BASE_URL}/ratings/${userId}/`);
};

export const reactToRating = async (
  userId: number,
  movieId: number,
  reactorId: number,
  type: 'agree' | 'disagree'
) => {
  return axios.post(
    `${BASE_URL}/ratings/${userId}/${movieId}/reaction`,
    { reactor_id: reactorId, reaction_type: type }
  );
};

export const fetchUserReactions = (reactorId: number) => {
  return axios.get(`${BASE_URL}/reactions/${reactorId}`);
};
