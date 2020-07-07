import React from 'react';
import { Link } from 'react-router-dom';


const HomePage = () => (
  <div>
    <h1 className ="page-title"> Pearish </h1>
    <Link to="/login">Login</Link>
    <Link to="/about">About</Link>
  </div>
);
/*
class App extends Component {
  render () {
    return (
      <div class="container">
	       <div class="row">
	        <div class="col-md-6">
	         <form method="post" action="#" id="#">
              <div class="form-group files">
                <label>Upload Your File </label>
                <input type="file" class="form-control" multiple="" />
              </div>


          </form>


	         </div>
	          <div class="col-md-6">
	           <form method="post" action="#" id="#">




              <div class="form-group files color">
                <label>Upload Your File </label>
                <input type="file" class="form-control" multiple="" />
              </div>


          </form>


	         </div>
	          </div>
            </div>
    );
  }
}
*/
export default HomePage;
