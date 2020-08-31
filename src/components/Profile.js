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
      user_items: []
    };
    this.renderEditable = this.renderEditable.bind(this);
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

  // function to delete the row and send a delete request and update the table
  deleteRow(name, email) {
    axios
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
      });
    })
    .catch((error) => {
      console.log(error);
      alert("Could not delete data");
    })}; 

// function send a get request for items, verify the user and update the state with user_items
  getItem(email) {
    axios
      .get("/users/" + encodeURIComponent(email.email))
      .then((response) => {
        const user_items = response.data
        console.log("USER ITEMS", user_items.user_items);
        console.log(user_items.user_items.length);
        const realData = []
        for (let item in user_items.user_items){
          realData.push(user_items.user_items[item]);
        }
        this.setState({user_items: realData});
        console.log("STATE VLUES", this.state.user_items)
      })
      .catch(() => {
        alert("Could not get data");
      });
  }

  // this function to be used for future inline editing
  renderEditable(cellInfo) {
    return (
      <div
        style={{ backgroundColor: "#fafafa" }}
        contentEditable
        suppressContentEditableWarning
        onBlur={e => {
          const data = [...this.state.user_items];
          data[cellInfo.index][cellInfo.column.id] = e.target.innerHTML;
        }}
        dangerouslySetInnerHTML={{
          __html: this.state.user_items[cellInfo.index][cellInfo.column.id]
        }}
      />
    )
  }

  render() {
    const columns = [
      {
        Header: "Name",
        accessor: "name",
        style: {
          textAlign: "center",
        },
        Cell: this.renderEditable,
      },
      {
        Header: "Category",
        accessor: "category",
        style: {
          textAlign: "center",
        },
        Cell: this.renderEditable,
      },
      {
        Header: "Purchased",
        accessor: "purchase_date",
        style: {
          textAlign: "center",
        },
        filterable: false,
        Cell: this.renderEditable,
      },
      {
        Header: "Expires",
        accessor: "expiration_date",
        style: {
          textAlign: "center",
        },
        filterable: false,
        Cell: this.renderEditable,
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
        Cell: this.renderEditable,
      },
      {
        Header: "Actions",
        Cell: (props) => {
          return (
            <div style={{display: 'flex', justifyContent: 'space-around'}}>
              {/* FUTURE EDIT BUTTON */}
            {/* <button 
            style={{ backgroundColor: "#008CBA", color: "#fefefe" }}
            >
              Edit
            </button> */}
            <button
              style={{ backgroundColor: "red", color: "#fefefe" }}
              onClick={() => {
                const token = window.localStorage.getItem("usertoken");
                const decoded = jwt_decode(token);
                const email = decoded.identity.email;
                this.deleteRow(props.original, email);
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
      // this.state.user_items !== [] &&
      (<div className="container">
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
            data = {this.state.user_items}
            filterable
            defaultPageSize={10}
            noDataText={"Please wait while we get your pantry"}
          ></ReactTable>
        </div>
        <UploadForm email={this.state.email}></UploadForm>
      </div>)
    );
  }
}

export default Profile;