import os
import sys

from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

Base = declarative_base()

class UserAccount(Base):
    __tablename__ = 'user_accounts'

    id = Column(Integer, primary_key=True)
    ip = Column(String(15), nullable=False)
    email = Column(String(50), nullable=False)
    password = Column(String(10), nullable=False)
    encrypted = Column(String(300), nullable=False)
    user_games = relationship("UserGames", back_populates="user_accounts")
    creation_date = Column(DateTime(timezone=True), server_default=func.now())

    # def __repr__(self):
    #     return "<User(id='%s', games='%s')>" % ( self.id, self.user_games )


class Games(Base):
    __tablename__ = 'games'

    id = Column(Integer, primary_key=True)
    title = Column(String(250), nullable=False)
    image_url = Column(String(1000), nullable=False)
    creation_date = Column(DateTime, nullable=False)


class UserGames(Base):
    __tablename__ = 'user_games'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user_accounts.id'))
    user_accounts = relationship(UserAccount, back_populates="user_games")
    game_id = Column(Integer, ForeignKey('games.id'))
    games = relationship(Games)
    gamer_name = Column(String(50), nullable=False)
    location = Column(String(10), nullable=False)
    creation_date = Column(DateTime, nullable=False)

# class LeagueOfLegendsPlayers(Base):
#     __tablename__ = 'league_of_legends_players'

#     id = Column(Integer, primary_key=True)
#     user_id = Column(Integer, ForeignKey('user_accounts.id'))
#     user_accounts = relationship(UserAccount)
#     account_id = Column(Integer, nullable=False)
#     summoner_level = Column(Integer, nullable=False)
#     creation_date = Column(DateTime, nullable=False)

Engine = create_engine('postgres://localhost:5434/pvp')
Base.metadata.create_all(Engine)