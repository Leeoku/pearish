import React from 'react';
import { Link } from 'react-router-dom';


const HomePage = () => (
  <div>
    <h1 className ="page-title"> Pearish </h1>
    <Link to="/login">Login</Link>
    <Link to="/about">About</Link>
  </div>
);

export default HomePage;
