from models import *
from sqlalchemy import create_engine, or_

engine = create_engine('sqlite:///sports.db')

Session = sessionmaker(bind=engine)
session = Session()

def return_teams_for_new_york():
    # here we want to return all teams that are associated with New York City
    return session.query(City).filter_by(name='New York').all()[0].teams

def return_players_for_la_dodgers():
    # here we want to return all players that are associated with the LA dodgers
    return session.query(Team).filter_by(name='Dodgers').all()[0].players

def return_sorted_new_york_knicks():
    # here we want to return all the players on the New York Knicks
    # sorted in ascending (small -> big) order by their number
    knicks = session.query(Team).filter_by(name='Knicks').all()[0].players
    sorted_list = sorted(knicks, key=lambda player: player.number)
    return sorted_list

def return_youngest_basket_ball_player_in_new_york():
    # here we want to sort all the players on New York Knicks by age
    # and return the youngest player
    knicks = session.query(Team).filter_by(name='Knicks').all()[0].players
    obj_age_dict = {player:player.age for player in knicks}
    return min(obj_age_dict, key = obj_age_dict.get)

def return_all_players_in_los_angeles():
    # here we want to return all players that are associated with
    # a sports team in LA
    return session.query(City).filter_by(name='Los Angeles').all()[0].teams[0].players + session.query(City).filter_by(name='Los Angeles').all()[0].teams[1].players

def return_tallest_player_in_los_angeles():
    # here we want to return the tallest player associted with
    # a sports team in LA
    la_players = return_all_players_in_los_angeles()
    obj_height_dict = {player:player.height for player in la_players}
    return max(obj_height_dict, key = obj_height_dict.get)

def return_team_with_heaviest_players():
    # here we want to return the team with the players that
    # have the heaviest average weight (total weight / total players)
    avg_weight_tups = session.query(Player.team_id,func.avg(Player.weight)).group_by(Player.team_id).all()
    heaviest_team = max(avg_weight_tups)[0]
    return session.query(Team).all()[heaviest_team-1]
