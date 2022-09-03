# Backend - Trivia API

## Setting up the Backend

### Install Dependencies

1. **Python 3.7** - Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

2. **Virtual Environment** - We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organized. Instructions for setting up a virual environment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

3. **PIP Dependencies** - Once your virtual environment is setup and running, install the required dependencies by navigating to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

#### Key Pip Dependencies

- [Flask](http://flask.pocoo.org/) is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use to handle the lightweight SQL database. You'll primarily work in `app.py`and can reference `models.py`.

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross-origin requests from our frontend server.

### Set up the Database

With Postgres running, create a `trivia` database:

```bash
createbd trivia
```

Populate the database using the `trivia.psql` file provided. From the `backend` folder in terminal run:

```bash
psql trivia < trivia.psql
```

### Run the Server

From within the `backend` directory first ensure you are working using your created virtual environment.

Yous should create `.env` file which should contain database configuration. Se below for an example that should be putted in the `.env` file.

````bash
DATABASE_NAME='database_name'
DATABASE_NAME_TEST='database_test_name'
DATABASE_USER='user'
DATABASE_PASSWORD='password'
````
To run the server, execute one by one these command below:
#### On linux or mac
```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```
#### On Windows
```bash
set FLASK_APP=flaskr
set FLASK_ENV=development
$env:FLASK_APP="flaskr"
flask run
```

## API Documentation

- This section will describe how to use each endpoints endpoints. In the last section, you will find how to test those endpoints.
- Base URL: At present this app can only be run locally and is not hosted as a base URL. The backend app is hosted at the default, `http://127.0.0.1:5000/`, which is set as proxi in the fronted configuration.
- Authentication: This version of the application does not require authentication or API keys.

### Error Handling

Errors are returned as JSON objects in the following format:
```json
{
  "success": False, 
  "error": 404, 
  "message": "resource not found"
}
```
The API will return three error types when requests fail:
- 400: Bad Request
- 404: Ressource Not Found
- 422: Not Processible
- 405: "Method Not Allowed

### Endpoints

`GET '/categories'`

- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a single key, categories, that contains an object of id: category_string key:value pairs.

```json
{
  "1": "Science",
  "2": "Art",
  "3": "Geography",
  "4": "History",
  "5": "Entertainment",
  "6": "Sports"
}
```


`GET '/questions?page=${integer}'`

- Fetches a paginated set of questions, a total number of questions, all categories and current category string.
- Request Arguments: `page` - integer
- Returns: An object with 10 paginated questions, total questions, object including all categories, and current category string.

```json
{
    "questions": [
        {
            "id": 1,
            "question": "This is a question",
            "answer": "This is an answer",
            "difficulty": 5,
            "category": 2
        },
    ],
    "totalQuestions": 100,
    "categories": { "1" : "Science",
    "2" : "Art",
    "3" : "Geography",
    "4" : "History",
    "5" : "Entertainment",
    "6" : "Sports" },
    "currentCategory": "History"
}
```


`GET '/categories/${id}/questions'`

- Fetches questions for a cateogry specified by id request argument.
- Request Arguments: `id` - integer
- Returns: An object with questions for the specified category, total questions, and current category string

```json
{
    "questions": [
        {
            "id": 1,
            "question": "This is a question",
            "answer": "This is an answer",
            "difficulty": 5,
            "category": 4
        },
    ],
    "totalQuestions": 100,
    "currentCategory": "History"
}
```


`DELETE '/questions/${id}'`

- Deletes a specified question using the id of the question
- Request Arguments: `id` - integer
- Returns: Does not need to return anything besides the appropriate HTTP status code. Optionally can return the id of the question. If you are able to modify the frontend, you can have it remove the question using the id instead of refetching the questions.


`POST '/quizzes'`

- Sends a post request in order to get the next question
- Request Body

```json
{
    "previous_questions": [1, 4, 20, 15],
    "quiz_category": {
        "id": 1,
        "type": "Science"
    }
 }
```

- Returns: a single new question object

```json
{
    "question": {
        "id": 1,
        "question": "This is a question",
        "answer": "This is an answer",
        "difficulty": 5,
        "category": 4
    }
}
```


`POST '/questions'`

- Sends a post request in order to add a new question
- Request Body:
```json
{
    "question":  "Heres a new question string",
    "answer":  "Heres a new answer string",
    "difficulty": 1,
    "category": 3,
}
```

- Returns: Does not return any new data



`POST '/questions'`

- Sends a post request in order to search for a specific question by search term
- Request Body:
```json
{
    "searchTerm": "this is the term the user is looking for"
}
```
- Returns: any array of questions, a number of totalQuestions that met the search term and the current category string

```json
{
    "questions": [
        {
            "id": 1,
            "question": "This is a question",
            "answer": "This is an answer",
            "difficulty": 5,
            "category": 5
        },
    ],
    "totalQuestions": 100,
    "currentCategory": "Entertainment"
}
```


## Testing

To deploy the tests, run

```bash
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```
