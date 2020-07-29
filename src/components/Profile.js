import React, { Component } from "react";
import jwt_decode from "jwt-decode";
import axios from "axios";
import UserItem from "./UserItem";
import Table from "react-bootstrap/Table";
import Accordion from "react-bootstrap/Accordion";
import Card from "react-bootstrap/Card";

class Profile extends Component {
  constructor() {
    super();
    this.state = {
      first_name: "",
      last_name: "",
      email: "",
      items: [],
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
    this.getItem({
      email: decoded.identity.email,
    });
  }

  getItem(email) {
    axios
      .get("http://localhost:5000/users/" + encodeURIComponent(email.email))
      .then((response) => {
        const user_items = response.data;
        console.log(user_items);
        JSON.stringify(user_items);
        console.log(JSON.stringify(user_items));
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
        <Accordion>
          <Card>
            <Accordion.Toggle as={Card.Header} eventKey="0">
              Your Profile
            </Accordion.Toggle>
            <Accordion.Collapse eventKey="0">
              <Card.Body>
                <div className="jumbotron mt-5">
                  <div className="col-sm-8 mx-auto">
                    <h1 className="text-center">Your Profile</h1>
                  </div>
                  <Table striped border hover>
                    <tbody>
                      <tr>
                        <td>Name</td>
                        <td>
                          {this.state.first_name} {this.state.last_name}
                        </td>
                      </tr>
                      <tr>
                        <td>Email</td>
                        <td>{this.state.email}</td>
                      </tr>
                    </tbody>
                  </Table>
                </div>
              </Card.Body>
            </Accordion.Collapse>
          </Card>
        </Accordion>
        <Table>
          <UserItem />
        </Table>
      </div>
    );
  }
}

export default Profile;
