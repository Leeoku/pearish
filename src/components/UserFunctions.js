import axios from "axios";

// Axios register call to get a post request for register
export const register = (newUser) => {
  return axios
      .post("/users/register", {
      first_name: newUser.first_name,
      last_name: newUser.last_name,
      email: newUser.email,
      password: newUser.password,
    })
    .then((response) => {
      console.log("Registered");
    });
};
// Axios register call to get a post request for login
export const login = (user) => {
  return axios
      .post("/users/login", {
      email: user.email,
      password: user.password,
    })
    .then((response) => {
      window.localStorage.setItem("usertoken", response.data.token);
      return response.data.token;
    })
    .catch((err) => {
      console.log(err);
    });
};
