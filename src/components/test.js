
import { getUser, deleteUser } from '../service/user';
import { getUserItem } from './^untitled:Untitled-1';
import { deleteUserItem } from './^untitled:Untitled-1';

class Profile extends Component {
  constructor() {
    super();
    this.state = {
      first_name: "",
      last_name: "",
      email: "",
      user_items: [],
      isInEditMode: false
    };
    this.renderEditable = this.renderEditable.bind(this); // this line needed for renderEditTable
  }

  componentDidMount() {
    const token = window.localStorage.getItem("usertoken");
    const decoded = jwt_decode(token);
    this.setState({
      first_name: decoded.identity.first_name,
      last_name: decoded.identity.last_name,
      email: decoded.identity.email,
    });
    const { data: { user_items }} = await getUserItem(decoded.identity.email);
    this.setState({ user_items });
  }

  renderEditable = (cellInfo) => {
    return (
      <div
        style={{ backgroundColor: "#fafafa" }}
        contentEditable
        suppressContentEditableWarning
        onBlur={e => {
          const user_items = [...this.state.user_items];
          data[cellInfo.index][cellInfo.column.id] = e.target.innerHTML;
          this.setState({ user_items });
        }}
        dangerouslySetInnerHTML={{
          __html: this.state.user_items[cellInfo.index][cellInfo.column.id]
        }}
      />
    );
  }

  async deleteItem(name, email) {
    try {
      await deleteUserItem(email, name);
      const user_items = this.state.user_items.filter(item => item.name === name);
      this.setState({ user_items });
    } catch (err) {
      console.log('Something went wrong', err);
    }
  }

  render() {
    const columns = [
      {
        Header: "Name",
        accessor: "name",
        style: {
          textAlign: "center",
        },
        // Cell: this.renderEditable,
      },
      {
        Header: "Category",
        accessor: "category",
        style: {
          textAlign: "center",
        },
        // Cell: this.renderEditable,
      },
      {
        Header: "Purchased",
        accessor: "purchase_date",
        style: {
          textAlign: "center",
        },
        filterable: false,
        // Cell: this.renderEditable,
      },
      {
        Header: "Expires",
        accessor: "expiration_date",
        style: {
          textAlign: "center",
        },
        filterable: false,
        // Cell: this.renderEditable,
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
        // Cell: this.renderEditable,
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
                const email = decoded.identity.email;
                this.deleteItem(props.original, email);
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
            // data = {user_items}
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

