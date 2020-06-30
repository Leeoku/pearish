import axios from 'axios';

export default {
  user: {
    login: (credentials) => axios.post('api/auth', {credentials}).then(
      response => response.data.user
    )
  }
};
