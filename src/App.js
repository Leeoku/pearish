import React from 'react';
import logo from './logo.svg';
import './App.css';

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <p>
          Edit <code>src/App.js</code> and save to reload.
        </p>
        <a
          className="App-link"
          href="https://reactjs.org"
          target="_blank"
          rel="noopener noreferrer"
        >
          Learn React
        </a>
      </header>
    </div>
  );
}

export default App;

 <input type="file" name="file" onChange={this.onChangeHandler}/>
 onChangeHandler=event=>{

    console.log(event.target.files[0])

}

<button type="button" class="btn btn-success btn-block"
onClick={this.onClickHandler}>Upload</button>

onClickHandler = () => {
    const data = new FormData()
    data.append('file', this.state.selectedFile)
}

import axios from 'axios';

axios.post("http://localhost:8000/upload", data, { // receive two parameter endpoint url ,form data
    })
    .then(res => { // then print response status
      console.log(res.statusText)
    })

    onClickHandler = () => {
     const data = new FormData()
     data.append('file', this.state.selectedFile)
     axios.post("http://localhost:8000/upload", data, {
        // receive two    parameter endpoint url ,form data
    })
    .then(res => { // then print response status
    console.log(res.statusText)
 })
}
