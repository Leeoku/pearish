const baseUrl = 'http://localhost:5000';

export const getUser = async id => {
  return axios.get(`${baseUrl}/users/${encodeURIComponent(id)}`);
}

export const deleteUser = async id => {
  return axios.delete(`${baseUrl}/users/${encodeURIComponent(id)}`);
}