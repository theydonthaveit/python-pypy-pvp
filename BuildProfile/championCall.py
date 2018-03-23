import requests
from urllib.parse import urljoin

def championCall(summonerID):
    BASE_URL = 'https://euw1.api.riotgames.com/lol/champion-mastery/v3/champion-masteries/by-summoner/%s' % (summonerID)
    headers = {
        "Origin": 'null',
        "Accept-Charset": "application/x-www-form-urlencoded; charset=UTF-8",
        "X-Riot-Token": 'RGAPI-1c02343a-7b7c-411c-9968-5cc7ddc6545a',
        "Accept-Language": "en-GB,en;q=0.5",
    }
    r = requests.get(BASE_URL, headers=headers)
    return r.json()

def championDetailCall(championID):
    BASE_URL = 'https://euw1.api.riotgames.com/lol/static-data/v3/champions/%s' % (championID)
    headers = {
        "Origin": 'null',
        "Accept-Charset": "application/x-www-form-urlencoded; charset=UTF-8",
        "X-Riot-Token": 'RGAPI-1c02343a-7b7c-411c-9968-5cc7ddc6545a',
        "Accept-Language": "en-GB,en;q=0.5",
    }
    r = requests.get(BASE_URL, headers=headers)
    return r.json()