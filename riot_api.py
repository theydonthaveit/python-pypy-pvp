import requests
import json
from octopus import Octopus
from urllib.parse import urljoin
from pprint import pprint
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Engine, UserAccount, GamerProfile
from BuildProfile.initialCall import initialCall
from BuildProfile.matchCall import matchCall, recentMatchCall, matchDetailCall, playerHistory
from BuildProfile.tierCall import tierCall
from BuildProfile.championCall import championCall, championDetailCall

Base.metadata.create_all(Engine)

DBsession = sessionmaker(bind=Engine)
session = DBsession()

init_call_DICT = initialCall('meow side')
champion_resp_DICT = championCall(init_call_DICT['id'])
champion_detail_resp_DICT = championDetailCall(champion_resp_DICT[0]['championId'])
tier_resp_DICT = tierCall(init_call_DICT['id'])
match_recent_resp_DICT = recentMatchCall(init_call_DICT['accountId'])

# {
#     "profileIconId": 3233,
#     "name": "meow side",
#     "summonerLevel": 56,
#     "accountId": 234897405,
#     "id": 102738872,
#     "revisionDate": 1521662452000
# }

# [{
# 'championId': 18,
# 'championLevel': 5,
# 'championPoints': 24852,
# 'lastPlayTime': 1521285782000
# }]

# [{'leagueName': "Nami's Knights",
# 'tier': 'SILVER',
# 'queueType': 'RANKED_SOLO_5x5',
# 'leaguePoints': 38,
# 'wins': 74,
# 'losses': 80,
# 'veteran': True,
# 'inactive': False,
# 'freshBlood': False,
# 'hotStreak': False}]

# {'matches':
# [{'platformId': 'EUW1',
# 'gameId': 3572662936,
# 'champion': 21,
# 'queue': 420,
# 'season': 11,
# 'timestamp': 1521660278674,
# 'role': 'DUO_CARRY',
# 'lane': 'BOTTOM'}],
# 'startIndex': 0,
# 'endIndex': 20,
# 'totalGames': 148}

