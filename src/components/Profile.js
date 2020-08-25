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
      // user_items: {data: []}
      user_items: []
    };
    this.renderEditable = this.renderEditable.bind(this);
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
    // this.setState({"name": "salami", "category": "placeholder", "purchase_date": "07/21/20", "expiration_date": "08/04/20", "count": 3})
    axios
      // .get("http://localhost:5000/users/" + encodeURIComponent(email.email))
      .get("/users/" + encodeURIComponent(email.email))
      .then((response) => {
        const user_items = response.data
        // this.setState(user_items)
        // const {user_items} = response.data;
        console.log("USER ITEMS", user_items.user_items);
        console.log(user_items.user_items.length);
        const realData = []
        const entry = user_items.user_items.forEach(entry=> console.log(entry));
        for (let item in user_items.user_items){
          // console.log(user_items.user_items[item]);
          // for (let index in item){
          //   realData.push(item[index])
          realData.push(user_items.user_items[item]);
        }

        // JSON.stringify(user_items);
        // console.log("JSON STRING",JSON.stringify(user_items));
        // this.setState({user_items: realData})
        // this.setState(user_items);
        this.setState({user_items: realData});

        // const nestedData = []
        // const stack = user_items.user_items.forEach(function(entry){
        //   console.log(entry);
        //   nestedData.push(entry)
        // });
        // console.log("STACK", stack);
        // console.log("NESTED DATA", nestedData);
        // this.setState({user_items: user_items})
        // const email_array = Object.values(email);
        // console.log("EMAIL ARRAY", email_array);
        console.log("STATE VLUES", [this.state])
      })
      .catch(() => {
        // console.log(console.error());
        alert("Could not get data");
      });
  }
      // getItem(email) {
      //   axios
      //     .get("/users/" + encodeURIComponent(email.email))
      //     .then((response) => {
      //       const {user_items} = response.data.user_items;
      //       this.setState({user_items});
      //       console.log("Data received", this.state.user_items);
      //       console.log("STATE VLUES", this.state)
      //     })
      //     .catch(() => {
      //       alert("Could not get data");
      //     });
      // }
  renderEditable(cellInfo) {
    return (
      // console.log("PRE RENDER", this.state.user_items[0]),
      <div
        style={{ backgroundColor: "#fafafa" }}
        contentEditable
        suppressContentEditableWarning
        onBlur={e => {
          const data = [...this.state.user_items];
          // console.log("EDIT DATA", data)
          data[cellInfo.index][cellInfo.column.id] = e.target.innerHTML;
          // this.setState({ data });
          // this.setState({ user_items: data });
        }}
        dangerouslySetInnerHTML={{
          // __html: this.state.data[cellInfo.index][cellInfo.column.id]
          __html: this.state.user_items
        }}
      />
    )
  }

  // if (this.state.user_items!== []) {
  render() {
    const {data } = this.state;
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
            // data = {user_items}
            // data={{"data":this.state.user_items}}
            data = {this.state.user_items}
            // data={this.state.items}
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