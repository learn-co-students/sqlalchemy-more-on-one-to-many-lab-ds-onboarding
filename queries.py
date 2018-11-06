from models import *
from sqlalchemy import create_engine
from sqlalchemy import func

engine = create_engine('sqlite:///sports.db')

Session = sessionmaker(bind=engine)
session = Session()


def return_teams_for_new_york():
    # here we want to return all teams that are associated with New York City
    ny = session.query(City).filter(City.name == "New York").one()
    return session.query(Team).filter(Team.city == ny).all()

def return_players_for_la_dodgers():
    # here we want to return all players that are associated with the LA dodgers
    q = session.query(Player,Team.name).filter(Team.name == "Dodgers").all()
    return [x[0] for x in q]


def return_sorted_new_york_knicks():
    # here we want to return all the players on the New York Knicks
    # sorted in ascending (small -> big) order by their number
    knicks = session.query(Team).filter(Team.name == "Knicks").one()
    return session.query(Player).filter(Player.team == knicks).order_by(Player.number.asc()).all()

def return_youngest_basket_ball_player_in_new_york():
    # here we want to sort all the players on New York Knicks by age
    # and return the youngest player
    # basketball = session.query(Sport).filter(Sport.name == "Basketball")
    # new_york = session.query(City).filter(City.name == "New York")
    # team = session.query(Team).filter(Team.city == new_york)
    # youngest = session.query(Player,City,Sport).filter(Sport.name== "Basketball").filter(City.name == "New York").order_by(Player.age.asc()).all()
    youngest2 = session.query(Player).join(City,Sport).filter(Sport.name=="Basketball").filter(City.name == "New York").order_by(Player.age.asc()).all()
    return youngest2

def return_all_players_in_los_angeles():
    # here we want to return all players that are associated with
    # a sports team in LA

    players_city = session.query(Player,City.name).filter(City.name == "Los Angeles").all()
    players = [x[0] for x in players_city]
    return players

def return_tallest_player_in_los_angeles():
    # here we want to return the tallest player associted with
    # a sports team in LA
    return session.query(Player,City.name).filter(City.name == "Los Angeles").order_by(Player.height.desc()).all()[0][0]

def return_team_with_heaviest_players():
    # here we want to return the city with the players that
    # have the heaviest average weight (total weight / total players)
    # return session.query(Team,func.avg(Player.weight).label('avg_weight')).group_by(Player.team).all()

    teams = session.query(Team).all()
    team_dict = {}
    for team in teams:
        team_dict[team] = session.query(Team,func.avg(Player.weight)).filter(Player.team == team).all()[0][1]

    heaviest_team = max(team_dict.items(),key = lambda kv: kv[1])
    return heaviest_team
