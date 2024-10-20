import axios from 'axios';

const API_URL = "http://localhost:5001"; // Replace with your backend URL

export const getRecommendations = async (data) => {
  const response = await axios.post(`${API_URL}/recommendations`, data, {
    headers: {
      'Content-Type': 'multipart/form-data'
    }
  });
  return response.data;
};

export const removeTracks = async (tracks) => {
  const response = await axios.post(`${API_URL}/remove_tracks`, { tracks });
  return response.data;
};
