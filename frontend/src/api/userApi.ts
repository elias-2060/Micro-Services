import axios from 'axios';

const BASE_URL = 'http://localhost:5001';

export const registerUser = (username: string, password: string) =>
  axios.post(`${BASE_URL}/users/`, { username, password });

export const loginUser = (username: string, password: string) =>
  axios.post(`${BASE_URL}/login`, { username, password });

export const fetchFriends = (userId: number) =>
  axios.get(`${BASE_URL}/users/${userId}/friends/`);

export const addFriend = (userId: number, friendId: number) =>
  axios.post(`${BASE_URL}/users/${userId}/friends/`, { friend_id: friendId });