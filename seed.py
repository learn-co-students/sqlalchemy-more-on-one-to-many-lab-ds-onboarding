from models import *
from sqlalchemy import create_engine
import pandas as pd

engine = create_engine('sqlite:///sports.db')

Session = sessionmaker(bind=engine)
session = Session()

# below we are reading the csv files to create the data we will need to create the players
# pandas returns a DataFrame object from reading the CSV
# we then tell the DataFrame object to turn each row into dictionaries
# by giving to_dict the argument "orient='records'"
# we are telling our DataFrame to make each row a dictionary using the column headers
# as the keys for the key value pairs in each new dictionary
# feel free to uncomment lines 18-21 to see each step of the process in your terminal
# ____ example ______
# la_dodgers0 = pd.read_csv('la_dodgers_baseball.csv')
# la_dodgers1 = pd.read_csv('la_dodgers_baseball.csv').to_dict()
# la_dodgers2 = pd.read_csv('la_dodgers_baseball.csv').to_dict(orient='records')
# import pdb; pdb.set_trace()
# __________________
la_dodgers = pd.read_csv('la_dodgers_baseball.csv').to_dict(orient='records')
la_lakers = pd.read_csv('la_lakers_basketball.csv').to_dict(orient='records')
ny_yankees = pd.read_csv('ny_yankees_baseball.csv').to_dict(orient='records')
ny_knicks = pd.read_csv('ny_knicks_basketball.csv').to_dict(orient='records')


# now that we have the data for each player
# add and commit the players, teams, sports and cities below
# we will need to probably write at least one function to iterate over our data and create the players
# hint: it may be a good idea to create the Teams, Cities, and Sports first

def heightconvert(height):
    string = ''.join(char for char in height if char.isalnum())
    feet = int(string[0])
    inches = int(string[1:])
    return feet * 12 + inches

### Creating Sports
basketball = Sport(name='Basketball')
baseball = Sport(name='Baseball')
sports = [basketball,baseball]

### Creating Cities
los_angeles = City(name='Los Angeles', state='California')
new_york = City(name='New York', state='New York')

cities = [los_angeles,new_york]
### Creating Teams
dodgers = Team(name='Dodgers', sport = baseball, city = los_angeles)
lakers = Team(name='Lakers',sport = basketball, city=los_angeles)
yankees = Team(name='Yankees', sport=baseball, city=new_york)
knicks = Team(name='Knicks', sport=basketball, city=new_york)

teams = [dodgers, lakers, yankees, knicks]



if len(session.query(Team).all()) == 0:
    session.add_all(teams)
    session.commit()




if len(session.query(City).all()) == 0:
    session.add_all(cities)
    session.commit()




if len(session.query(Sport).all()) == 0:
    session.add_all(sports)
    session.commit()

### len(session.query(TABLE).all()) is to ensure that each of the tables are
### empty before we actually create them

#### To make this more D.R.Y , you could make a function add_items
"""
def add_items(table,list_of_items):
    if len(session.query(table).all()) == 0:
        session.add_all(list_of_items)
        session.commit()
add_items(Sport,sports)
add_items(City,cities)
add_items(Team,teams)
"""

for player in la_dodgers:
    session.add(Player(name=player['name'],number=player['number'],height=heightconvert(player['height']), weight=player['weight'],age=(118-int(player['birthdate'][-2:])),team=dodgers))
    session.commit()

for player in la_lakers:
    session.add(Player(name=player['name'],number=player['number'],height=heightconvert(player['height']), weight=player['weight'],age=player['age'],team=lakers))
    session.commit()

for player in ny_yankees:
    session.add(Player(name=player['name'],height=heightconvert(player['height']), weight=player['weight'],age=player['age'],team=yankees))
    session.commit()

for player in ny_knicks:
    session.add(Player(name=player['name'],number=player['number'],height=heightconvert(player['height']), weight=player['weight'],age=player['age'],team=knicks))
    session.commit()
