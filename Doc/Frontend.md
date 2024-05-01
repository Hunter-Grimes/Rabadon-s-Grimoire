# Frontend
### Overview
This is file by file explantion on what the role each file on the frontend folder has on the app, for a less thourough explanation on what the role of the Frontend is visit the [Getting Started](./Technical.md#AppFrontend) file.
### [asyncWorker.py](/exeFrontend/asyncWorker.py)
Facilitates the offloading of computationally intensive tasks to a different thread.
### [callLocalRiotAPI.py](/exeFrontend/callLocalRiotAPI.py)
Uses Willump to get the necessary data for the user.
### [championStatsWidget.py](/exeFrontend/championStatsWidget.py)
File in charge of displaying the champion stats in widget form
### [champStatsPage.py](/exeFrontend/champStatsPage.py)
Similar to the championStatsWidget it displays the champion stats but in an expanded page form. 
### [dataFiles.py](/exeFrontend/dataFiles.py)
file with the function find_data_file in charge of finding data file using file name
### [fetchData.py](/exeFrontend/fetchData.py)
Uses find_data_file in combination with the user, creating a visually pleasing and easy to understand presentation of such data for the user.
### [leagueOverlay.py](/exeFrontend/leagueOverlay.py)
Currently unused feature that could be implemented in future versions that acts as an overlay for LOL.
### [LoadingIndicator.py](/exeFrontend/LoadingIndicator.py)
File in charge of using the Loading Indicator while the app is getting the information requested.
### [lobbyPage.py](/exeFrontend/lobbyPage.py)
File in charge of the page for when user is in a lobby, the way it looks and how it navigates.    
### [main.py](/exeFrontend/main.py)
Like the app.py file in the backend, this fullfills the same purpuse of running and containing everything in one place.
### [matchHistory.py](/exeFrontend/matchHistory.py)
Visually shows to the user of the app the informations about their match history, with im
### [patchNotesPage.py](/exeFrontend/patchNotesPage.py)
Currently unused feature that could be implemented in future versions for telling the user information about the updates and changes to the app.
### [profilePage.py](/exeFrontend/profilePage.py)
File in charge of the profile page which is essentially the page that focuses on giving the user all of the data obtained for them.
### [runeSuggestion.py](/exeFrontend/runeSuggestion.py)
This file is in charge of the suggestion of possible runes for the user. 
### [setup.py](/exeFrontend/setup.py)
This creates the executable file, it is not included as part of the app, but it is a necessary part for the current version of the project.
### [tabStyle.qss](/exeFrontend/tabStyle.qss)
Defines the way each part of the tabs of the app looks, the color the size, the placement.
### [userTags.py](/exeFrontend/userTags.py)
Displays the user tags obtained through the Riot API.