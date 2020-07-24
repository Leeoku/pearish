import React, { Component } from "react";
import jwt_decode from "jwt-decode";
import axios from "axios";

class Profile extends Component {
  constructor() {
    super();
    this.state = {
      first_name: "",
      last_name: "",
      email: "",
    };
  }

  componentDidMount() {
    const token = window.localStorage.getItem("usertoken");
    const decoded = jwt_decode(token);
    this.setState({
      first_name: decoded.identity.first_name,
      last_name: decoded.identity.last_name,
      email: decoded.identity.email,
    });
  }

  getItem() {
    axios
      .get("http://localhost:5000/user/ken@gmail.com")
      .then((response) => {
        const user_items = response.user_items;
        console.log(user_items);
        JSON.stringify(user_items);
        this.setState(user_items);
        console.log("Data received");
      })
      .catch(() => {
        console.log(console.error());
        alert("Could not get data");
      });
  }
  render() {
    return (
      <div className="container">
        <div className="jumbotron mt-5">
          <div className="col-sm-8 mx-auto">
            <h1 className="text-center">PROFILE</h1>
          </div>
          <table className="table col-md-6 mx-auto">
            <tbody>
              <tr>
                <td>First Name</td>
                <td>{this.state.first_name}</td>
              </tr>
              <tr>
                <td>Last Name</td>
                <td>{this.state.last_name}</td>
              </tr>
              <tr>
                <td>Email</td>
                <td>{this.state.email}</td>
              </tr>
              <tr>
                <td>Items</td>
                <td>
                  {this.state.user_items.map((user_item) => (
                    <getItem user_item={user_item} />
                  ))}
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    );
  }
}

export default Profile;
