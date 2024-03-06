from dotenv import load_dotenv, find_dotenv
import os
import requests

def getSumByName(name):
    load_dotenv()
    api_key = os.getenv('RIOT_API_KEY')

    requestURL = "https://na1.api.riotgames.com/lol/summoner/v4/summoners/by-name/"
    
    requestURL = requestURL + name
    
    requestURL = requestURL + '?api_key=' + api_key

    response = requests.get(requestURL)
    
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception("Bad or No Response")