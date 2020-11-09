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

### Backend Dependencies and Steps

1. Install postgresSQL and run the following command to check if it has been successfully configured
    `psql --version`

2. Make databases for both the development and tests by running the following command
    * `createdb -U postgres trivia`
    * `createdb -U postgres trivia_test`

2. setup the virtual enviroment by the following command
    * first install virtualenv by running the commnad `pip3 install virtualenv`
    * Intialize the virtualenv by running the command `virtualenv backend`

3. Install all the dependencies by running following command
    `pip install -r requirements.txt`

4. Run the migrations 
    `flask db migrate` and after that `flask db upgrade`

5. Run the development server by running following commands
    * Set the FLASK_APP and FLASK_ENV envir variable by `SET FLASK_APP=flaskr` or `SET FLASK_ENV=development`
    * Run the backend server by `flask run`


### Frontend Dependencies and Steps

The `./frontend` directory contains a complete React frontend to consume the data from the Flask server.

1. Install the dependencies by running the command below:
    `npm install`
2. Run the frontend server by `npm start` this command runs the start script described in the package.json file



## API Refrence

### Getting Started
* BASE URL: Currently this application is hosted only locally. The backend is hosted at http://localhost:5000/
* Authentication: This version does not require authentication or api keys.



### API Endpoints

### GET /categories

* Returns all the categories
* Sample URL : `http://localhost:5000/categories`

Response Example

```javascript
{
    "success":true,
    "categories_count":3,
    "categories":[
        {
            "id":1,
            "type:"history"
        },
        {
            "id":2,
            "type":"geography"
        }
    ]
}
```


### GET /questions
    
Details
* Returns the list of questions
* Returned questions are paginated in a group of 10
* Also returns the list of categories and total questions count

Sample URL : `http://localhost:5000/questions` or `http://localhost:5000/questions?page=1` 

Response Example

```javascript
{   
    "success":true,
    "categories":[
        {
            "id":1,
            "type":"geography"
        },
        {
            "id":2,
            "type":"history"
        }
    ],
    "questions":[
        {
        "question":"What is the national sports of India",
        "answer":"Hockey",
        "category":"sports",
        "difficulty":1,
        "id":1
        },
        {
        "question":"Who was the first prime minister of India",
        "answer":"Jawaharlal Nehru",
        "category":"history",
        "difficulty":2,
        "id":2
        },
        ...
        {
        "question":"Asian games last held in India",
        "answer":"1982",
        "category":"sports",
        "difficulty":2,
        "id":3
        }
    ],
    "total_questions":20
}
```

### POST /questions

Details:
* Insert 1 question or find the questions based on the json data parsed with the request

Sample URL `http://localhost:5000/questions`

Example Request JSON data

1. Searching for the questions based on the keyword 

```javascript
    {
     "keyword":"Who"   
    }
```

OR

2. Inserting questions with the relative fields

```javascript{

    {
        "question":"who was the first prime minister of India?",
        "answer":"Jawaharlal Nehru",
        "category":3,
        "rating":4,
        "difficulty":3
    }

}
```


Response Example

1. Getting the questions based on the keyword if any otherwise throw 404
```javascript
    {
        "questions":[
            {
                "question":"who was the first prime minister of India?"
                "answer":"Jawaharlal Nehru",
                "category":"history",
                "difficulty":3,
                "rating":4,
                "id":2
            }
        ],
        "questions_count":1,
        "success":true
    }
```

2. Getting the success message and id after adding the question

```javascript
    {
        "success":true,
        "question_id":2
    }

```


### POST /categories/<category_id>/questions

Details:
* Returns all the questions in the category and the category fields
* Returns the count of the questions in the category

SAMPLE URL: `http://localhost:5000/categories/1/questions` where 1 is <category_id>

Response Example


```javascript

    {
        "current_category":{
            "id":1,
            "type":"Geography"
        },
        "questions":[
        {
        "question":"What is the national sports of India",
        "answer":"Hockey",
        "category":"sports",
        "difficulty":1,
        "id":1
        },
        {
        "question":"Who was the first prime minister of India",
        "answer":"Jawaharlal Nehru",
        "category":"history",
        "difficulty":2,
        "id":2
        },
        {
        "question":"Asian games last held in India",
        "answer":"1982",
        "category":"sports",
        "difficulty":2,
        "id":3
        }
        ],
        "total_questions":3,
        "success":true
    }


```

### DELETE /questions/<question_id>

Details
* Delete the question based on the question_id parsed as a url parameter <question_id>

Sample URL `http://localhost:5000/questions/1` where 1 is the <question_id>

Example Response

```javascript
    {
        "success":true,
        "question_id":1
    }
```


### POST /quizzes

Details:
* Get the random question based on the category and previous_questions if any
* If total questions in the category are less than total questions asked in quiz it will return no question

Sample URL `http://localhost:5000/quizzes`

Example JSON Request Data 

```javascript
    {
        "quiz_category":1,
        "prev_questions":[
            {
                "id":1,
                "question":"Who was the first Prime Minister of India ?",
                "answer":"Jawaharlal Nehru",
                "rating":"3",
                "difficulty":"4"
                "category":"history"
            }
        ]
    }
```

Response Example

```javascript

    {
        "success":true,
        "question":{
            "id":2,
            "question":"The Battle of Plassey was fought in",
            "answer":"1974",
            "category":"history",
            "rating":"3",
            "difficulty":"5"
        }
    }


```


### Run Test Suites
All the api endpoints tests are written in test_flaskr.py to confirm the valid response on each request.
You need to follow following steps to run tests.
1. Create a test db using createdb command `createdb -U postgres trivia_test`
2. Run the test by entering the command `python test_flaskr.py`



### Error Handling
This version currently handles 3 main types of errors:
* 400 - BAD REQUESTION
* 404 - RESOURCES NOT FOUND
* 422 - UNPROCESSABLE
    
Errors are retured in JSON in the following structured way
```javascript
    {
        "status_code":404,
        "success":false,
        "message":"resource not found"
    }
```


## Credits

This api(__init__.py), test suits(test_flaskr.py) and this README is developed and documented by kartik Ahuja
All the other things like react based frontend and models are provided by the udacity for the students as a project template for UDACITY FULL STACK NANAODEGREE PROGRAME