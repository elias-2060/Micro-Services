import axios from 'axios';

const BASE_URL = 'http://localhost:5006';

export const fetchMovies = (start = 0, count = 10) =>
  axios.get(`${BASE_URL}/movies/`, { params: { start, count } });

export const fetchMovieById = (id: number) =>
  axios.get(`${BASE_URL}/movie/${id}/`);
