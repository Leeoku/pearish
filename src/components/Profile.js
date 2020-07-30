import React, { Component } from "react";
import jwt_decode from "jwt-decode";
import axios from "axios";
import Table from "react-bootstrap/Table";
import Accordion from "react-bootstrap/Accordion";
import Card from "react-bootstrap/Card";
import ReactTable from "react-table-6";
import UploadForm from "./UploadForm";

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

  deleteRow(name) {
    const index = this.state.uesr_items.findIndex((user_items) => {
      return user_items.name === name;
    });
    console.log("index", index);
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
    const columns = [
      {
        Header: "Name",
        accessor: "name",
        style: {
          textAlign: "center",
        },
      },
      {
        Header: "Category",
        accessor: "category",
        style: {
          textAlign: "center",
        },
      },
      {
        Header: "Purchased",
        accessor: "purchase_date",
        style: {
          textAlign: "center",
        },
        filterable: false,
      },
      {
        Header: "Expires",
        accessor: "expiration_date",
        style: {
          textAlign: "center",
        },
        filterable: false,
      },
      {
        Header: "Quantity",
        accessor: "count",
        style: {
          textAlign: "center",
        },
        sortable: false,
        filterable: false,
        width: 100,
        maxwidth: 100,
        minWidth: 100,
      },
      {
        Header: "Actions",
        Cell: (props) => {
          return (
            <button
              style={{ backgroundColor: "red", color: "#fefefe" }}
              onClick={() => {
                this.deleteRow(props.original.name);
              }}
            >
              Delete
            </button>
          );
        },
        sortable: false,
        filterable: false,
      },
    ];
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
        <div>
          <ReactTable
            columns={columns}
            data={this.state.user_items}
            filterable
            defaultPageSize={5}
            noDataText={"Please wait while we get your pantry"}
          ></ReactTable>
        </div>
        <UploadForm email={this.state.email}></UploadForm>
      </div>
    );
  }
}

export default Profile;
