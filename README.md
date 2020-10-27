# Full Stack Trivia Project

This is a Trivia full stack project, which is basically a game where user can test their knowledge by answering the questions, The main purpose of this project is to create a api and test suite for implementing the following functionality:

1) Display questions - both all questions and by category. Questions should show the question, category and difficulty rating by default and can show/hide the answer. 
2) Delete questions.
3) Add questions and require that they include question and answer text.
4) Search for questions based on a text query string.
5) Play the quiz game, randomizing either all questions or within a specific category. 


## Getting Started 

Developers using this repo should already have installed python3,pip,node and npm.

## About the Stack

In this project flask,sqlalchemy,postgress are used for the backend and react,bootstrap used for the frontend.

### Backend Dependencies

1. setup the virtual enviroment

``


### Frontend Dependencies

The `./frontend` directory contains a complete React frontend to consume the data from the Flask server. You will need to update the endpoints after you define them in the backend. Those areas are marked with TODO and can be searched for expediency. 

Pay special attention to what data the frontend is expecting from each API response to help guide how you format your API. 

[View the README.md within ./frontend for more details.](./frontend/README.md)


## API Refrence

### Getting Started
    * BASE URL: Currently this application is hosted only locally. The backend is hosted at http://localhost:5000/
    * Authentication: This version does not require authentication or api keys.
### Error Handling
    This version currently handles 3 main types of errors:
        * 400 - BAD REQUESTION
        * 404 - RESOURCES NOT FOUND
        * 422 - UNPROCESSABLE
    
    Errors are retured in JSON in the following structured way
        ```json
            {
                "error":404,
                "success":false,
                "message":"resource not found"
            }
        ``` 
