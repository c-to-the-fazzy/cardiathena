from tictactoe import RandomTicTacToeAgent, TicTacToeAdjudicator, TicTacToeGameManager


# Create the players, the adjudicator, and the game object.
agent_1 = RandomTicTacToeAgent()
agent_2 = RandomTicTacToeAgent()
adj = TicTacToeAdjudicator()
game = TicTacToeGameManager(agent_list=[agent_1, agent_2],
                            adjudicator=adj)

# Play a game.
game.play_game()

# Put a debug point here to inspect the game object.
input()
