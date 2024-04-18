from dotenv import load_dotenv
import os
import requests
from HandleError import riotApiError as apiError

load_dotenv()
api_key = os.getenv('RIOT_API_KEY')


def getAccountByPUUID(PUUID):
    BASE_URL = "https://americas.api.riotgames.com/riot/"
    
    requestURL = BASE_URL + "account/v1/accounts/by-puuid/"
    
    requestURL = requestURL + PUUID
    
    response = requests.get(requestURL, headers={"X-Riot-Token": api_key})
    
    if response.status_code == 200:
        return response.json()
    else:
        apiError(response.status_code)


def getACCTInfoByRiotID(tagLine, gameName):
    BASE_URL = "https://americas.api.riotgames.com/riot/"
    
    requestURL = BASE_URL + "account/v1/accounts/by-riot-id/"
    
    requestURL = requestURL + gameName + '/' + tagLine
    
    response = requests.get(requestURL, headers={"X-Riot-Token": api_key})
    
    if response.status_code == 200:
        return response.json()
    else:
        apiError(response.status_code)


def getSummonerByPUUID(PUUID):
    BASE_URL = "https://na1.api.riotgames.com/lol/"
    
    requestURL = BASE_URL + "summoner/v4/summoners/by-puuid/"
    
    requestURL = requestURL + PUUID
    
    response = requests.get(requestURL, headers={"X-Riot-Token": api_key})
    
    if response.status_code == 200:
        return response.json()
    else:
        apiError(response.status_code)


def getMatchLast20(PUUID):
    BASE_URL = "https://americas.api.riotgames.com/lol/"
    
    requestURL = BASE_URL + "match/v5/matches/by-puuid/"
    
    requestURL = requestURL + PUUID
    
    requestURL = requestURL + '/ids'
    
    response = requests.get(requestURL, headers={"X-Riot-Token": api_key})
    
    if response.status_code == 200:
        return response.json()
    else:
        apiError(response.status_code)


def getMatchXtoX(PUUID, x, y):
    BASE_URL = "https://americas.api.riotgames.com/lol/"
    
    requestURL = BASE_URL + "match/v5/matches/by-puuid/"
    
    requestURL = requestURL + PUUID
    
    requestURL = requestURL + '/ids' + '?start=' + str(x) + '&count=' + str((y-x))
    
    response = requests.get(requestURL, headers={"X-Riot-Token": api_key})
    
    if response.status_code == 200:
        return response.json()
    else:
        apiError(response.status_code)

      
def getMatchByMatchID(GID):
    BASE_URL = "https://americas.api.riotgames.com/lol/"
    
    requestURL = BASE_URL + "match/v5/matches/"

    requestURL = requestURL + GID

    response = requests.get(requestURL, headers={"X-Riot-Token": api_key})

    if response.status_code == 200:
        return response.json()
    else:
        apiError(response.status_code)
        

def getMatchTimeLineByMatchID(GID):
    BASE_URL = "https://americas.api.riotgames.com/lol/"

    requestURL = BASE_URL + "match/v5/matches/"

    requestURL = requestURL + GID

    requestURL = requestURL + '/timeline'

    response = requests.get(requestURL, headers={"X-Riot-Token": api_key})

    if response.status_code == 200:
        return response.json()
    else:
        apiError(response.status_code)

  
def getLeagueInfoBySID(SID):
    BASE_URL = "https://na1.api.riotgames.com/lol/"

    requestURL = BASE_URL + "league/v4/entries/by-summoner/"

    requestURL = requestURL + SID

    response = requests.get(requestURL, headers={"X-Riot-Token": api_key})

    if response.status_code == 200:
        return response.json()
    else:
        apiError(response.status_code)
       