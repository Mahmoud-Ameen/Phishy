import axios from 'axios';

const api = axios.create({
  baseURL: 'https://exact-hound-rationally.ngrok-free.app',
  headers: {
    'ngrok-skip-browser-warning': 'true',
    'Content-Type': 'application/json',
  },
  withCredentials: true,
});

export default api;