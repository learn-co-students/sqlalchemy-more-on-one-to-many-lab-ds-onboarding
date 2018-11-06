from models import *
from sqlalchemy import create_engine
import pandas as pd

engine = create_engine('sqlite:///sports.db')

Session = sessionmaker(bind=engine)
session = Session()

# below we are reading the csv files to create the data we will need to create the players
# pandas returns a DataFrame object from reading the CSV
# we then tell the DataFram
# e object to turn each row into dictionaries
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

la = City(name = 'Los Angeles')
ny = City(name = 'New York')
# session.add(la)
# session.add(ny)

baseball = Sport(name = 'Baseball')
basketball = Sport(name = 'Basketball')
# session.add(baseball)
# session.add(basketball)


dodgers = Team(name ="Dodgers",city =la,sport=baseball)
lakers = Team(name = "Lakers",city=la,sport=basketball)
yankees = Team(name = "Yankees",city=ny,sport=baseball)
knicks = Team(name = "Knicks",city=ny,sport=basketball)

# session.add_all([dodgers,lakers,yankees,knicks])

##adding teams to cities

# la.teams = [dodgers,lakers]
# ny.teams = [yankees, knicks]
# session
##adding teams to Sports

# baseball.teams = [dodgers,yankees]
# basketball.teams = [lakers,knicks]


# session.add_all([la,ny])
# session.add_all([baseball,basketball])
# session.commit()

def height_fixer(str_height):
    if "'" in str_height:
        height_list = str_height.split("'")
    else:
        height_list = str_height.split("-")

    inches = int(height_list[0].strip())*12 + int(height_list[1].strip(' "'))
    return inches



def number_fixer(team_data,category):
    total = 0
    length = 0
    for p in team_data:
        try:
            total+= int(p[category])
            length +=1
        except:
            continue

    average = total/length

    return

def team_creator(team_object,team_data):
    list_players = []
    for player in team_data:
        if 'age' in player:
            try:
                player['age'].isnumeric()
                age_player = int(player['age'])
            except:
                age_player = player['age']
        else:
            age_player = None
        if 'number' in player:
            try:
                player['number'].isnumeric()
                num = int(player['number'])
            except:
                num = player['number']
        else:
            num = None
        star = Player(name=player['name'],height=height_fixer(player['height']),\
        weight=player['weight'],number=num,age=age_player,team=team_object)

        list_players.append(star)
    team_object.players = list_players
    return team_object

all_teams_data = [la_dodgers,la_lakers,ny_yankees,ny_knicks]
team_classes = [dodgers,lakers,yankees,knicks]
combined_data = zip(team_classes,all_teams_data)

teams_to_commit = []
for team_class,team_data in combined_data:
    teams_to_commit.append(team_creator(team_class,team_data))


session.add_all(teams_to_commit)
session.commit()



# now that we have the data for each player
# add and commit the players, teams, sports and cities below
# we will need to probably write at least one function to iterate over our data and create the players
# hint: it may be a good idea to creat the Teams, Cities, and Sports first
