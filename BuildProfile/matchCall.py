import requests
import json
from urllib.parse import urljoin

def matchCall(accountID):
    BASE_URL = 'https://euw1.api.riotgames.com/lol/match/v3/matchlists/by-account/%s' % (accountID)
    headers = {
        "Origin": 'null',
        "Accept-Charset": "application/x-www-form-urlencoded; charset=UTF-8",
        "X-Riot-Token": 'RGAPI-1c02343a-7b7c-411c-9968-5cc7ddc6545a',
        "Accept-Language": "en-GB,en;q=0.5",
    }
    r = requests.get(BASE_URL, headers=headers)
    return r.json()

def recentMatchCall(accountID):
    BASE_URL = 'https://euw1.api.riotgames.com/lol/match/v3/matchlists/by-account/%s/recent' % (accountID)
    headers = {
        "Origin": 'null',
        "Accept-Charset": "application/x-www-form-urlencoded; charset=UTF-8",
        "X-Riot-Token": 'RGAPI-1c02343a-7b7c-411c-9968-5cc7ddc6545a',
        "Accept-Language": "en-GB,en;q=0.5",
    }
    r = requests.get(BASE_URL, headers=headers)
    return r.json()

def playerHistory():
    BASE_URL = 'https://euw1.api.riotgames.com/lol/match/v1/stats/player_history/EUW1/32142316'
    headers = {
        "Origin": 'null',
        "Accept-Charset": "application/x-www-form-urlencoded; charset=UTF-8",
        "X-Riot-Token": 'RGAPI-1c02343a-7b7c-411c-9968-5cc7ddc6545a',
        "Accept-Language": "en-GB,en;q=0.5",
    }
    r = requests.get(BASE_URL, headers=headers)
    return r.json()

def matchDetailCall(matchID):
    BASE_URL = 'https://euw1.api.riotgames.com/lol/match/v3/matches/%s' % (matchID)
    headers = {
        "Origin": 'null',
        "Accept-Charset": "application/x-www-form-urlencoded; charset=UTF-8",
        "X-Riot-Token": 'RGAPI-1c02343a-7b7c-411c-9968-5cc7ddc6545a',
        "Accept-Language": "en-GB,en;q=0.5",
    }
    r = requests.get(BASE_URL, headers=headers)
    with open('data.json', 'w') as outfile:
        json.dump(r.json(), outfile)

    return r.json()