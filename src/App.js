import React from 'react';
import {  Route } from 'react-router-dom';
import HomePage from './components/pages/HomePage';
import LoginPage from './components/pages/LoginPage';
import AboutPage from './components/pages/AboutPage';
import'semantic-ui-css/semantic.min.css';
const App = () => (
    <div class = "ui secondary menu">
      <NavLink
            class = "active item"
         href = "/" >Home</NavLink>
      <NavLink
            class ="item"
         href = "/login">Login</NavLink>
      <NavLink
            class = "item"
         href = "/about">About</NavLink>
        <Route path="/" exact component={HomePage} />
        <Route path="/login" exact component={LoginPage} />
        <Route path="/about" exact component={AboutPage} />
    </div>
);

export default App;
