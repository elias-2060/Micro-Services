import axios from 'axios';

const BASE_URL = 'http://localhost:5005';

export const fetchNewsfeed = (userId: number) =>
  axios.get(`${BASE_URL}/newsfeed/${userId}/`);
