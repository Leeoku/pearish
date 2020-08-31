import React, { Component } from "react";
import PearishCarousel from "./Carousel";

class Landing extends Component {
  render() {
    return (
      <div className="container">
        <div className="jumbotron mt-5">
          <div className="col-sm-8 mx-auto">
            <h1 className="text-center">WELCOME TO YOUR DIGITAL PANTRY</h1>
          </div>
        </div>
        <div>
          <PearishCarousel></PearishCarousel>
        </div>
      </div>
    );
  }
}

export default Landing;
