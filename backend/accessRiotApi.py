from dotenv import load_dotenv
import os
import requests
from HandleError import riotApiError as apiError

load_dotenv()
api_key = os.getenv('RIOT_API_KEY')


def getAccountByPUUID(PUUID):
    BASE_URL = "https://americas.api.riotgames.com/riot/"
    
    requestURl = BASE_URL + "account/v1/accounts/by-puuid/"
    
    requestURl = requestURl + PUUID
    
    requestURl = requestURl + '?api_key=' + api_key
    
    response = requests.get(requestURl)
    
    if response.status_code == 200:
        return response.json()
    else:
        apiError(response.status_code)


def getACCTInfoByRiotID(tagLine, gameName):
    BASE_URL = "https://americas.api.riotgames.com/riot/"
    
    requestURl = BASE_URL + "account/v1/accounts/by-riot-id/"
    
    requestURl = requestURl + gameName + '/' + tagLine
    
    requestURl = requestURl + '?api_key=' + api_key

    response = requests.get(requestURl)
    
    if response.status_code == 200:
        return response.json()
    else:
        apiError(response.status_code)


def getSummonerByName(name):
    BASE_URL = "https://na1.api.riotgames.com/lol/"
    
    requestURL = BASE_URL + "summoner/v4/summoners/by-name/"
    
    requestURL = requestURL + name
    
    requestURL = requestURL + '?api_key=' + api_key

    response = requests.get(requestURL)
    
    if response.status_code == 200:
        return response.json()
    else:
        apiError(response.status_code)


def getSummonerByPUUID(PUUID):
    BASE_URL = "https://na1.api.riotgames.com/lol/"
    
    requestURL = BASE_URL + "summoner/v4/summoners/by-puuid/"
    
    requestURL = requestURL + PUUID
    
    requestURL = requestURL + '?api_key=' + api_key

    response = requests.get(requestURL)
    
    if response.status_code == 200:
        return response.json()
    else:
        apiError(response.status_code)


def getMatchLast20(PUUID):
    BASE_URL = "https://americas.api.riotgames.com/lol/"
    
    requestURL = BASE_URL + "match/v5/matches/by-puuid/"
    
    requestURL = requestURL + PUUID
    
    requestURL = requestURL + '/ids'
    
    requestURL = requestURL + '?api_key=' + api_key
    

    response = requests.get(requestURL)
    
    if response.status_code == 200:
        return response.json()
    else:
        apiError(response.status_code)


def getMatchXtoX(PUUID, x, y):
    BASE_URL = "https://americas.api.riotgames.com/lol/"
    
    requestsURL = BASE_URL + "match/v5/matches/by-puuid/"
    
    requestsURL = requestsURL + PUUID
    
    requestsURL = requestsURL + '/ids' + '?start=' + str(x) + '&count=' + str((y-x))
    
    requestsURL = requestsURL + '&api_key=' + api_key
    
    response = requests.get(requestsURL)
    
    if response.status_code == 200:
        return response.json()
    else:
        apiError(response.status_code)

      
def getMatchByMatchID(GID):
    BASE_URL = "https://americas.api.riotgames.com/lol/"
    
    requestURL = BASE_URL + "match/v5/matches/"

    requestURL = requestURL + GID

    requestURL = requestURL + '?api_key=' + api_key

    response = requests.get(requestURL)

    if response.status_code == 200:
        return response.json()
    else:
        apiError(response.status_code)
        

def getMatchTimeLineByMatchID(GID):
    BASE_URL = "https://americas.api.riotgames.com/lol/"

    requestURL = BASE_URL + "match/v5/matches/"

    requestURL = requestURL + GID

    requestURL = requestURL + '/timeline'

    requestURL = requestURL + '?api_key=' + api_key

    response = requests.get(requestURL)

    if response.status_code == 200:
        return response.json()
    else:
        apiError(response.status_code)

  
def getLeagueInfoBySID(SID):
    BASE_URL = "https://na1.api.riotgames.com/lol/"

    requestURL = BASE_URL + "league/v4/entries/by-summoner/"

    requestURL = requestURL + SID

    requestURL = requestURL + '?api_key=' + api_key

    response = requests.get(requestURL)

    if response.status_code == 200:
        return response.json()
    else:
        apiError(response.status_code)
       