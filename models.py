from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

Base = declarative_base()


# write the Player, City, Sport and Team tables below

class Player(Base):
    __tablename__= "players"
    id = Column(Integer,primary_key=True)
    team_id = Column(Integer,ForeignKey('teams.id'))
    name = Column(String)
    number = Column(Integer)
    height = Column(Integer)
    weight = Column(Integer)
    age = Column(Integer)
    team = relationship("Team",back_populates="players")


# Name
# Number (if applicable)
# Height
# Weight
# Belongs to a team



class City(Base):
    __tablename__ = "cities"
    id = Column(Integer,primary_key=True)
    name = Column(String)
    state = Column(String)
    teams = relationship("Team",back_populates="city")

# City(Base):
# Name
# State
# Has many teams


class Sport(Base):
    __tablename__ = "sports"
    id = Column(Integer,primary_key=True)
    name = Column(String)
    teams = relationship("Team", back_populates="sport")


#
# Sport(Base):
# Name
# Has many teams


class Team(Base):
    __tablename__ = "teams"
    id = Column(Integer,primary_key=True)
    city_id = Column(Integer,ForeignKey('cities.id'))
    sport_id = Column(Integer,ForeignKey('sports.id'))
    name = Column(String)
    city = relationship("City", back_populates="teams")
    sport = relationship("Sport",back_populates="teams")
    players = relationship("Player",back_populates= "team")

# Team(Base):
# Name
# Belongs to a city
# Belongs to a sport
# Has many players





engine = create_engine('sqlite:///sports.db')
Base.metadata.create_all(engine)
