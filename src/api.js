import axios from "axios";

export default {
  user: {
    login: (credentials) =>
      axios
        .post("http://localhost:6969/api/auth", { credentials })
        .then((response) => response.data.user),
  },
};
