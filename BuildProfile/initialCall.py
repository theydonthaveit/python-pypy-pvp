import requests
from urllib.parse import urljoin

def initialCall(playerName):
    BASE_URL = 'https://euw1.api.riotgames.com/lol/summoner/v3/summoners/by-name/%s' % (playerName)
    headers = {
        "Origin": 'null',
        "Accept-Charset": "application/x-www-form-urlencoded; charset=UTF-8",
        "X-Riot-Token": 'RGAPI-29c9b941-5090-4611-9c28-7fc5f1e86df8',
        "Accept-Language": "en-GB,en;q=0.5",
    }
    r = requests.get(BASE_URL, headers=headers)
    return r.json()