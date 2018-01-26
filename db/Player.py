import os
import sys

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

class PlayerLol(Base):
    __tablename__ = 'player_lol'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    account_id = Column(Integer, nullable=False)
    summoner_id = Column(Integer, nullable=False)

class PlayerMatches(Base):
    __tablename__ = 'player_matches'

    id = Column(Integer, primary_key=True)
    player = relationship(PlayerLol)
    player_id = Column(Integer, ForeignKey('payer_id'))

class PlayerStats(Base):
    __tablename__ = 'player_stats'

    id = Column(Integer, primary_key=True)
    player = relationship(PlayerLol)
    player_id = Column(Integer, ForeignKey('payer_id'))
    mmr = Column(Integer, default=1500)
    kda = Column(String(5), nullable=True)
    games = Column(Integer, nullable=True)
