import os
import sys

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

class UserAccount(Base):
    __tablename__ = 'user_accounts'

    id = Column(Integer, primary_key=True)
    ip = Column(String(15), nullable=False)
    email = Column(String(50), nullable=False)
    password = Column(String(10), nullable=False)
    encrypted = Column(String(300), nullable=False)


class Games(Base):
    __tablename__ = 'games'

    id = Column(Integer, primary_key=True)
    title = Column(String(250), nullable=False)
    image_url = Column(String(1000), nullable=False)


class UserGames(Base):
    __tablename__ = 'user_games'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user_accounts.id'))
    user_accounts = relationship(UserAccount)
    game_id = Column(Integer, ForeignKey('games.id'))
    games = relationship(Games)
    gamer_name = Column(String(50), nullable=False)
    location = Column(String(10), nullable=False)

Engine = create_engine('postgresql://localhost:5434/pvp')
Base.metadata.create_all(Engine)