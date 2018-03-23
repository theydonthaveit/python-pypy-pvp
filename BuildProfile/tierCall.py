import requests
from urllib.parse import urljoin

def tierCall(playerID):
    BASE_URL = 'https://euw1.api.riotgames.com/lol/league/v3/positions/by-summoner/%s' % (playerID)
    headers = {
        "Origin": 'null',
        "Accept-Charset": "application/x-www-form-urlencoded; charset=UTF-8",
        "X-Riot-Token": 'RGAPI-1c02343a-7b7c-411c-9968-5cc7ddc6545a',
        "Accept-Language": "en-GB,en;q=0.5",
    }
    r = requests.get(BASE_URL, headers=headers)
    return r.json()