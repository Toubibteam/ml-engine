## API

To **start** the API locally run `gunicorn app:api`. The entry point is http://localhost:8000/api by default.

To **test** the API, download [Postman](https://www.getpostman.com/). This tool is super convenient to make http request on demand :o. Open Postman and choose POST in the request type checklist. The body of the request must be

```json
{
  "diagnostic": "<your query>"
}
```

The output is an array of objects

```json
{
  "code_id": "The code DIMs and TIMs are looking for",
  "description": {
    "description": "The description of the code",
    "type": "Either CCAM or CIM"
  },
  "metric": "An indicator of how well the code matches the user's query. The higher the better"
}
```

## Details

- The directory `model` contains all model-specific logic
- The directory `docs` contains a demo of a client (to be hosted on github pages for instance)
- The directory `test` contains all the unit tests performed on the functions of the project
- The files `app.py` and `serve.py` are for the Falcon API
- The files `requirements.txt`, `runtime.txt` and `Procfile` are for deployment on Heroku


## Tests

For a better tracking of the bugs, a good pratice is to test the functions written in the packages.


#### Foreword

Each package has its own test file. The test files can be found in the `test` directory that clones the project architecture. They are names following the convention: `test_<name of the associated package>`.


#### Running the tests

All the tests can be run at once using the package `pytest` (get it by running `sudo pip install -U pytest` :o). Then, run the `pytest` command at the root of the project directory.


## Heroku

To commit latest changes to the online API on Heroku simply do

```
git add .
git commit -m "<new changes for deployment>"
git push heroku master
```
