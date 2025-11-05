from models import GameState, GameMove
import numpy as np

'''
decisionLogic will handle utility functions 
'''

# Heuristic functions to guess at the game score to decide what decisions to make

# Score based on large groups
def groupHeuristic(state : GameState):
    return None

# Score based on color sums
def colorHeuristic(state : GameState):
    return None

# Score based on size
def sizeHeuristic(state : GameState):
    return None

# Builds successor states based on current state and returns the children states
def generateSuccessors(state: GameState):
    return None

if __name__ == "__main__":
    print("decisionLogic test goes here")