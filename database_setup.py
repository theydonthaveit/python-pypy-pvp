import sys
import datetime

from flask_login import LoginManager, UserMixin
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base, declared_attr
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from passlib.hash import pbkdf2_sha512

Base = declarative_base()


class BaseMixin(object):

    @declared_attr
    def id(self):
        return Column(Integer, primary_key=True, unique=True)

    @declared_attr
    def created_at(self):
        return Column(DateTime, default=datetime.datetime.utcnow)

    @declared_attr
    def updated_at(self):
        return Column(DateTime, default=datetime.datetime.utcnow)


class UserAccount(Base, BaseMixin, UserMixin):
    __tablename__ = 'user_account'

    def __init__(self, username, passcode, mobile, email, ip_address):
        self.username = username
        self.password = pbkdf2_sha512.hash(passcode)
        self.mobile = mobile
        self.email = email
        self.ip_address = ip_address

    username = Column(String(80), nullable=False)
    password = Column(String(1000), nullable=False)
    mobile = Column(String(15), nullable=False, unique=True)
    email = Column(String(100), nullable=False, unique=True)
    ip_address = Column(String(15), nullable=False)
    is_verified = Column(Boolean, nullable=False, default=False)
    gamer_profile = relationship("GamerProfile", backref="user_account")

    def is_verified_check(self):
        return self.is_verified

    def decode_password(self, password):
        return pbkdf2_sha512.verify(password, self.password)


class GamerProfile(Base, BaseMixin):
    __tablename__ = 'gamer_profile'

    user = relationship("UserAccount", back_populates="gamer_profile")
    user_id = Column(Integer, ForeignKey('user_account.id'))
    game = Column(String(100), nullable=False)
    in_game_name = Column(String(100), nullable=False)
    country = Column(String(100), nullable=False)
    postal_code = Column(String(12), nullable=False)
    league_of_legends_profile = relationship("LeagueOfLegendsProfileBase", backref="gamer_profile")


class LeagueOfLegendsProfileBase(Base, BaseMixin):
    __tablename__ = 'league_of_legends_profile_base'

    gamer_id = Column(Integer, ForeignKey('gamer_profile.id'))
    account_id = Column(Integer, nullable=False)
    summoner_level = Column(Integer, nullable=False)
    summoner_id = Column(Integer, nullable=False)
    league_of_legends_champion_mastery = relationship("LeagueOfLegendsChampionMastery", backref="league_of_legends_profile_base")
    league_of_legends_league_position = relationship("LeagueOfLegendsLeaguePosition", backref="league_of_legends_profile_base")
    league_of_legends_match_list = relationship("LeagueOfLegendsMatchList", backref="league_of_legends_profile_base")


class LeagueOfLegendsChampionMastery(Base, BaseMixin):
    __tablename__ = 'league_of_legends_champion_mastery'

    league_of_legends_profile_base_id = Column(Integer, ForeignKey('league_of_legends_profile_base.id'))
    champion_id = Column(Integer, nullable=False)
    champion_level = Column(Integer, nullable=False)
    champion_points = Column(Integer, nullable=False)
    last_play_time = Column(Integer, nullable=False)
    league_of_legends_match_list = relationship("LeagueOfLegendsChampionInfo", backref="league_of_legends_champion_mastery")


class LeagueOfLegendsChampionInfo(Base, BaseMixin):
    __tablename__ = 'league_of_legends_champion_info'

    league_of_legends_champion_mastery_id = Column(Integer, ForeignKey('league_of_legends_champion_mastery.id'))
    name = Column(Integer, nullable=False)
    title = Column(Integer, nullable=False)


class LeagueOfLegendsLeaguePosition(Base, BaseMixin):
    __tablename__ = 'league_of_legends_league_position'

    league_of_legends_profile_base_id = Column(Integer, ForeignKey('league_of_legends_profile_base.id'))
    league_name = Column(String(50), nullable=False)
    tier = Column(String(20), nullable=False)
    queue_type = Column(String(10), nullable=False)
    league_Points = Column(Integer, nullable=False)
    wins = Column(Integer, nullable=False)
    losses = Column(Integer, nullable=False)
    veteran = Column(Boolean, nullable=False)


class LeagueOfLegendsMatchList(Base, BaseMixin):
    __tablename__ = 'league_of_legends_match_list'

    league_of_legends_profile_base_id = Column(Integer, ForeignKey('league_of_legends_profile_base.id'))
    game_id = Column(Integer, nullable=False)
    champion = Column(String(50), nullable=False)
    queue = Column(String(10), nullable=False)
    season = Column(Integer, nullable=False)
    timestamp = Column(Integer, nullable=False)
    role = Column(String(20), nullable=False)
    lane = Column(String(20), nullable=False)


Engine = create_engine('postgres://localhost:5434/pvp')
Base.metadata.create_all(Engine)