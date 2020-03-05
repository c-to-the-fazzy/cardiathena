import csv
import uuid
from datetime import datetime

from adjudicator.hearts_adjudicator import HeartsAdjudicator
from adjudicator.state import HeartsState
from agent.LowLayer import LowLayer
from agent.RandomHeartsAgent import RandomHeartsAgent
from base import GameManager
from database.MySql import MySQLDatabase as db
from database.MySql.MySQLVariables import CSV_DIR, INSERT_GAME

# Create the players, the adjudicator, and the game object.
game_uuid = uuid.uuid4().hex
adj = HeartsAdjudicator()
state = HeartsState()
agent_1 = RandomHeartsAgent()
agent_2 = RandomHeartsAgent()
agent_3 = LowLayer()
agent_4 = RandomHeartsAgent()
agent_list = [0, agent_1, agent_2, agent_3, agent_4]

game = GameManager(agent_list,
                   adjudicator=adj,
                   state=state)


def save_game():
    """
    The save_game() method saves information about the game before it starts. Information that is saved includes the game
    uuid to uniquely identify each game, the date and time a game starts, agent_types that will participate in the game.

    """
    time_stamp = datetime.now()
    id_list = list()

    # Gets the id of each agent type ie The Random Agent's id is 1 and appends to a list
    for agent in agent_list:
        if agent is not 0:
            id = agent.__dict__.get("id")
            id_list.append(id)

    # values is the data that will be saved
    values = (None, time_stamp, id_list[0], id_list[1], id_list[2], id_list[3], game_uuid)
    # Insert the game data into the database
    db.query_database(INSERT_GAME, values)


def process_state_data():
    """
    The process_state_data() method processes the state data to be stored in the MySQL database. The state data includes
    location of the cards: deck (numPy array converted to a python list), player actions: action, scores, and a game
    uuid. The method calls save_game() from the game manager which returns a list of dictionaries which contains
    deck, action, and score. In order to reduce overhead with multiple insertions, game state data is writen to a
    csv file which is then inserted into the database.

    """
    # Get state_data, list of dictionaries, from game manager's save_game()
    state_data = game.save_game()

    # Process state_data, insert into database
    directory = CSV_DIR + "{}.csv".format(game_uuid)
    with open(directory, 'w') as file:
        writer = csv.writer(file, lineterminator='\n',)
        writer.writerow(["deck", "action", "score", "game_uuid"])
        for data in state_data:
            deck = data["deck"].tolist()
            action = data["actions"]
            score = data["scores"]
            writer.writerow([deck, action, score, game_uuid])
    db.insert_state(directory)


# Save starting game information
save_game()

# Play a game.
game.play_game()

# The game is over, save the states of the game into the database.
process_state_data()

# Put a debug point here to inspect the game object.
#input()
