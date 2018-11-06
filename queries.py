from models import *
from sqlalchemy import create_engine, or_

engine = create_engine('sqlite:///sports.db')

Session = sessionmaker(bind=engine)
session = Session()

def return_teams_for_new_york():
    # here we want to return all teams that are associated with New York City

    ## other solution: session.query(City).filter_by(name='New York').first().teams
    return session.query(Team).join(City).filter(City.name == 'New York').all()


def return_players_for_la_dodgers():
    # here we want to return all players that are associated with the LA dodgers
    ## other solution: session.query(Team).filter_by(name='Dodgers').all()[0].players
    return session.query(Player).join(Team).filter(Team.name == 'Dodgers').all()


def return_sorted_new_york_knicks():
    # here we want to return all the players on the New York Knicks
    # sorted in ascending (small -> big) order by their number
    # other solutions
    """
    knicks = session.query(Team).filter_by(name='Knicks').all()[0].players
    sorted_list = sorted(knicks, key=lambda player: player.number)
    sorted_list
    """
    return session.query(Player).join(Team).filter(Team.name == 'Knicks').order_by(Player.age.asc()).all()

def return_youngest_basket_ball_player_in_new_york():
    # here we want to sort all the players on New York Knicks by age
    # and return the youngest player
    """
    knicks = session.query(Team).filter_by(name='Knicks').all()[0].players
    obj_age_dict = {player:player.age for player in knicks}
    min(obj_age_dict, key = obj_age_dict.get)
    """
    player_age = session.query(Player,func.min(Player.age)).join(Team).filter(Team.name == 'Knicks').first()
    return player_age[0]

def return_all_players_in_los_angeles():
    # here we want to return all players that are associated with
    # a sports team in LA

    return session.query(Player).join(Team).join(City).filter(City.name == 'Los Angeles')

def return_tallest_player_in_los_angeles():
    # here we want to return the tallest player associted with
    # a sports team in LA
    """
    la_players = return_all_players_in_los_angeles()
    obj_height_dict = {player:player.height for player in la_players}
    max(obj_height_dict, key = obj_height_dict.get)
    """

    tallest_player = session.query(Player,func.max(Player.height)).join(Team).join(City).filter(City.name=='Los Angeles').first()
    return tallest_player[0]

def return_team_with_heaviest_players():
    # here we want to return the team with the players that
    # have the heaviest average weight (total weight / total players)
    teams = session.query(Team).all()
    avg_weight_tups = []
    for team in teams:
        team_weight = session.query(Team,func.avg(Player.weight)).filter(Player.team == team ).first()
        avg_weight_tups.append(team_weight)
    heaviest_team = max(avg_weight_tups,key = lambda x: x[1])
    return heaviest_team[0]
