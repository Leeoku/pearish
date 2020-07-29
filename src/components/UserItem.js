import React, { Component } from "react";
import Accordion from "react-bootstrap/Accordion";
import Card from "react-bootstrap/Card";
import Table from "react-bootstrap/Table";

class UserItem extends Component {
  constructor(props) {
    super(props);
    this.state = {
      name: "",
      category: "",
      purchase_date: "red",
      expiration_date: "",
      count: 0,
    };
  }
  render() {
    return (
      <Accordion>
        <Card>
          <Accordion.Toggle as={Card.Header} eventKey="0">
            Your Pantry
          </Accordion.Toggle>
          <Accordion.Collapse eventKey="0">
            <Card.Body>
              <div className="jumbotron mt-5">
                <div className="col-sm-8 mx-auto">
                  <h1 className="text-center">Your Pantry</h1>
                </div>
                <Table striped border hover responsive>
                  <thread>
                    <tr>
                      <th>Name</th>
                      <th>Category</th>
                      <th>Purchase Date</th>
                      <th>Expiration Date</th>
                      <th>Count</th>
                    </tr>
                  </thread>
                </Table>
              </div>
            </Card.Body>
          </Accordion.Collapse>
        </Card>
      </Accordion>
    );
  }
}
export default UserItem;
