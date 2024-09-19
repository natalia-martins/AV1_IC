#Use o pacote:
from chrome_trex import DinoGame, ACTION_UP, ACTION_FORWARD, ACTION_DOWN

# Create a new game that runs with at most 'fps' frames per second.
# Use fps=0 for unlimited fps.
game = DinoGame(fps)

# Go to the next frame and take the action 'action'
# (ACTION_UP, ACTION_FORWARD or ACTION_DOWN).
game.step(action)

# Get a list of floats representing the game state
# (positions of the obstacles and game speed).
game.get_state()

# Get the game score.
game.get_score()

# Reset the game.
game.reset()

# Close the game.
game.close()

#Para executar vários jogadores ao mesmo tempo:
from chrome_trex import MultiDinoGame, ACTION_UP, ACTION_FORWARD, ACTION_DOWN

# Create a new game that runs with at most 'fps' frames per second.
# Use fps=0 for unlimited fps.
game = MultiDinoGame(fps)

# Go to the next frame and make each player take the corresponding
# action in  'action_list'
# (ACTION_UP, ACTION_FORWARD or ACTION_DOWN).
game.step(action_list)

# Get a list of floats representing the game state
# (positions of the obstacles and game speed).
game.get_state()

# Get a list with the score of each score of each player.
game.get_scores()

# Reset the game.
game.reset()

# Close the game.
game.close()