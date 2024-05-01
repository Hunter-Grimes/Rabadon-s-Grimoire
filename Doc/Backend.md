# Backend
### Overview
This is file by file explantion on what the role each file on the backend folder has on the app, for a less thourough explanation on what the role of the Backend is visit the [Getting Started](./Technical.md#AppBackend) file.
### [accessRiotApi.py](/backend/accessRiotApi.py)
This file contains all of the functions that make direct requests with the Riot API, as such any further additions of such functions should be added here as well (and of course has to follow)
*note currently requests are only being used on AMERICAS region and using NA1 routing value, though this could later be changed.
### [apiEndpoints.py](/backend/apiEndpoints.py)
This file regulates both the info that is put in the Riot API requests (things like PUUID and RIOT ID) and the info that is obtained from the requests (like match history and player stats).
### [apiHelpers.py](/backend/apiHelpers.py)
Sorts the data obtained into the different models on the database to be easily used and accessed.
### [app.py](/backend/app.py)
This essentially puts everything in the backend together to be easily used in one file, as such one needs to be sure any additions or changes in other files are accesible in this file.
### [docker-compose.yml](/backend/docker-compose.yml)

### [Dockerfile](/backend/Dockerfile)

### [extensions.py](/backend/extensions.py)
This files contains the extensions to flask and the declaration of variable sto be used accross the different files. While currently only containing flask related extensions and variables this is not limited only to flask and could also hold future needed extensions with their needed variable accross files. 
### [HandleError.py](/backend/HandleError.py)
This file should be very self explanatory, if an error occurs with accessing the Riot API it will return an error code, this file in turn will return what the error code means.
This means that unless a change occurs with the Riot API this file should probably remain unchanged as long as everything is up to date.
For an explanation on what each error code means and some common reasons for it visit the [Riot Documentation](https://developer.riotgames.com/docs/portal#web-apis_response-codes).
### [models.py](/backend/models.py)
As one could guess from the name, these are the models in which the data obtained from the API requests  is sorted into and is afterward uploaded to the database.
### [requirements.txt](/backend/requirements.txt)
Contains the requirements needed for the database to function smoothly.
### [RIOT_API_KEY.txt](/backend/RIOT_API_KEY.txt)
This is the project's Riot API key, currently it is using a personal key so it is set to a fixed rate. This probably should not be ever changed unless a Product API key is obtained.

#### Return to [Getting Started](Technical.md) page