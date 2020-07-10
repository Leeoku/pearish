import React from 'react';
import {  Route } from 'react-router-dom';
import HomePage from './components/pages/HomePage';
import LoginPage from './components/pages/LoginPage';
import AboutPage from './components/pages/AboutPage';
import'semantic-ui-css/semantic.min.css';
const App = () => (
    <div class = "ui secondary menu">
      <a>
            class = "active item"
         href = "/" >Home</a>
      <a>
            class ="item"
         href = "/login">Login</a>
      <a>
            class = "item"
         href = "/about">About</a>
        <Route path="/" exact component={HomePage} />
        <Route path="/login" exact component={LoginPage} />
        <Route path="/about" exact component={AboutPage} />
    </div>
);

export default App;
