import requests
import os

api_key = os.getenv('API_KEY')
url = 'https://americas.api.riotgames.com/riot/account/v1/accounts/by-riot-id/'
url2 = 'https://oc1.api.riotgames.com/lol/spectator/v5/active-games/by-summoner/'

def getPuuid(summonerName, tagLine):
    api_url = url + summonerName + '/' + tagLine + '?api_key=' + api_key
    resp = requests.get(api_url)

    playerInfo = resp.json()
    playerPuuid = playerInfo['puuid']
    return playerPuuid

def gametype(playerPuuid):
    spectator_url = url2 + playerPuuid + '?api_key=' + api_key
    resp2 = requests.get(spectator_url)
    gameInfo = resp2.json()
    try:
        gMode = gameInfo['gameMode']
        return str(gMode)
    except Exception:
        return None

