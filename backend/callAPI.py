from dotenv import load_dotenv
import os
import requests
from HandleError import riotApiError as apiError

load_dotenv()
api_key = os.getenv('RIOT_API_KEY')


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

      
def getMatchByMatchID(PUUID):
    BASE_URL = "https://americas.api.riotgames.com/lol/"
    
    requestURL = BASE_URL + "match/v5/matches/"

    requestURL = requestURL + PUUID

    requestURL = requestURL + '?api_key=' + api_key

    response = requests.get(requestURL)

    if response.status_code == 200:
        return response.json()
    else:
        apiError(response.status_code)