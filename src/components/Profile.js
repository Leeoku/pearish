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
      user_items: [],
    };
  }

  componentDidMount() {
    const token = window.localStorage.getItem("usertoken");
    const decoded = jwt_decode(token);
    // var decoded_email = Object.values(decoded.identity);
    // console.log("DECODE EMAIL", Object.values((decoded_email)));
    this.setState({
      first_name: decoded.identity.first_name,
      last_name: decoded.identity.last_name,
      email: decoded.identity.email,
      // email: Object.values(decoded.identity)
    });
    this.getItem({
      email: decoded.identity.email,
      // email: Object.values(decoded.identity),
    });
  }
 
  deleteRow(name, email) {
//     axios
//       .delete("http://localhost:5000/users/" + encodeURIComponent(email.email))
//       .then((response) => {
    //     const index = this.state.items.find((user_items) => {
    //       return user_items.name === name;

    // })
    // this.setState({items: name},() => console.log(this.state.items))
    // this.setState({items: name});
    // var array = this.state.items
    // console.log("ARRAY", array);
    // console.log("NAME", name);
    // console.log("DELETE ROW ARRAY", array.user_items);
    // console.log(email);
    axios
    // .delete("/users/" + "ken@gmail.com" + "/items",
    .delete("/users/" + encodeURIComponent(email) + "/items",
    {
      headers: {
        'Content-Type': 'application/json',
      },
      data: name
    })
    .then((response) => {
      const token = window.localStorage.getItem("usertoken");
      const decoded = jwt_decode(token);
      this.getItem({
        email: decoded.identity.email,
        // email: Object.values(decoded.identity)
      });
    })
    .catch((error) => {
      console.log(error);
      alert("Could not delete data");
    }); 

  // componentDidUpdate(prevProps, prevState){
  //   console.log("THIS STATE", this.state.items.constructor !== Array)
  //   console.log("THIS STATE", this.state.items)
  //   console.log("prev state", prevState.items)
  //   // if (this.state.items.constructor !== Array && this.state.items === prevState.items){
  //   //   console.log("State matches Item");
    // }
  }

  getItem(email) {
    axios
      // .get("http://localhost:5000/users/" + encodeURIComponent(email.email))
      .get("/users/" + encodeURIComponent(email.email))
      .then((response) => {
        const user_items = response.data;
        const email_array = Object.values(email);
        console.log("EMAIL", email);
        console.log("EMAIL ARRAY", email_array);
        console.log(user_items);
        JSON.stringify(user_items);
        console.log("JSON STRING",JSON.stringify(user_items));
        this.setState(user_items);
        // this.setState({user_items: user_items})
        console.log("Data received", this.state.user_items);
        console.log("Data received 2", this.state.items);
        console.log("STATE VLUES", this.state)
      })
      .catch(() => {
        // console.log(console.error());
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
            <div style={{display: 'flex', justifyContent: 'space-around'}}>
            <button 
            style={{ backgroundColor: "#008CBA", color: "#fefefe" }}
            >
              Edit
            </button>
            <button
              style={{ backgroundColor: "red", color: "#fefefe" }}
              onClick={() => {
                const token = window.localStorage.getItem("usertoken");
                const decoded = jwt_decode(token);
                // const email = Object.values(decoded.identity);
                const email = decoded.identity.email;
                this.deleteRow(props.original, email);
                // console.log("props", props.original)
              }}
            >
              Delete
            </button>
            </div>
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
                  <Table striped hover>
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
            // data={this.state.items}
            filterable
            defaultPageSize={10}
            noDataText={"Please wait while we get your pantry"}
          ></ReactTable>
        </div>
        <UploadForm email={this.state.email}></UploadForm>
      </div>
    );
  }
}

export default Profile;
