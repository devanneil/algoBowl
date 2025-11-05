import numpy as np

'''
models.py is where we can put any shared data strucutre, decisionTree and decisionLogic both depend on this
'''


# Game state for each node
class GameState:
    def __init__(self, board : np.ndarray, score=0, leafNode = False):
        self.board = board  # np array of integers representations of colors
        self.score = score  # integer score value of actual score

class GameMove:
    def __init__(self, x : int, y : int, color : int):
        self.x = x # Indexed at array 0
        self.y = y # Indexed at array 0
        self.color = color # Integer representation (1-8) of character