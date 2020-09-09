![Alt text](/pearish.png "Title")
# Pearish

## Project Overview
A digital pantry app to scan receipts and extract food items to a personal database. Users can easily check what food was recently purchased and when the food is expected to expire. This helps monitor grocery purchasing habits and reduce the chance of spoiled food.

* <a href = ''>Demo</a> 


### Current Status (v0)
This project is still in the development phase and growing to address the different complexities. Here are some features that are coming soon!
* Progressive web app using your webcam (possibly cell phone) to scan receipts
* Upgrading profile table using React hooks with in-line editing

## Technologies
* React.js with:
    * React-Table
    * Axios HTTP client
    * JWT-Decode to decode JWT tokens
* Python with:
    * Flask for REST APIs 
    * pandas to manipulate the database
    * bcrypt to hash passwords
    * OCR.space Image Recognition API
    * Spacy Natural Language Processing
* NGINX as a reverse proxy to handle requests
* MongoDB

## Architecture

Below shows the different Docker containers set up for this project.

![Alt text](/architecture.png "Title")


## Setup
* `docker-compose up --build` to build the container environments. Afterwards, `docker-compose up` will suffice

## Contributors
Omar, Tyler, Maaz, Avi, Ryan, Andrew and mentor Kevin