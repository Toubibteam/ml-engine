## Quickstart

To start the API locally

```
python app.py
```

To open a client in local

1. open `index.html`, line 45 change the url of the API
2. double-click on `index.html`


## Details

- The directory `model` contains all model-specific logic
- The directory `docs` contains a demo of a client (to be hosted on github pages for instance)
- The files `app.py` and `serve.py` are for the Flask API
- The files `requirements.txt`, `runtime.txt` and `Procfile` are for deployment on Heroku


## Heroku

To commit latest changes to the online API on Heroku simply do

```
git add .
git commit -m "new changes for deployment"
git push heroku master
```

## Github Pages

To commit the latest changes to the client simply do

```
git add .
git commit -m "new changes for clients"
git push origin master
```