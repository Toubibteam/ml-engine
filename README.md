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


## MongoDB

#### Set up

To run the project you first need to install a mongoDB server on your computer by following the instructions provided on their [website](https://docs.mongodb.com/).

#### Provide Database

To upload data to the database, use the `mongoimport` command:

`mongoimport -d <database> -c <collection> --file <json file>`

Here are the parameters used for the project:

- database: `codes`

- collections: `cim`, `ccam`

- json files: `CIM10.json`, `CCAM_V50.json`

You may need to add the `--jsonArray` option if the json has an array shape instead of a simple object.

#### Clean Database

`mongoimport` imports the data contained in the file in the specified collection without cleaning it before. If a clean is first required, use the `mongo` command to run the mongo shell. Once launched, proceed as follow:

1. switch to the right database: `use <database>`

2. clean the collection: `db.<collection>.drop()`

3. leave the shell: `Ctrl + d`

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

## External documentation

- [Understanding the *yield* keyword (stackoverflow)](https://stackoverflow.com/questions/231767/what-does-the-yield-keyword-do?page=1&tab=votes#tab-top)
