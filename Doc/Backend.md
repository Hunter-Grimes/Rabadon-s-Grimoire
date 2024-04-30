# Backend
### Overview
This is file by file explantion on what the role each file on the backend folder has on the app, for a less thourough explanation on what the role of the Backend is visit the [Getting Started](./Technical.md) file.
### [accessRiotApi.py](/backend/accessRiotApi.py)
This file contains all of the functions that make direct requests with the Riot API, as such any further additions
### [apiEndpoints.py](/backend/apiEndpoints.py)

### [apiHelpers.py](/backend/apiHelpers.py)

### [app.py](/backend/app.py)
This essentially puts everything in the backend together to be easily used in one file, as such one needs to be sure any additions or changes in other files are accesible in this file.
### [docker-compose.yml](/backend/docker-compose.yml)
### [Dockerfile](/backend/Dockerfile)
### [extensions.py](/backend/extensions.py)
### [HandleError.py](/backend/HandleError.py)
This file should be very self explanatory, if an error occurs with accessing the Riot API it will return an error code, this file in turn will return what the error code means.
This means that unless a change occurs with the Riot API this file should probably remain unchanged as long as everything is up to date.
For an explanation on what each error code means and some common reasons for it visit the [Riot Documentation](https://developer.riotgames.com/docs/portal#web-apis_response-codes).
### [models.py](/backend/models.py)
### [requirements.txt](/backend/requirements.txt)
### [RIOT_API_KEY.txt](/backend/RIOT_API_KEY.txt)
This is the project's Riot API key, currently it is using a personal key so it is set to a fixed rate. This probably should not be ever changed unless a Product API key is obtained.