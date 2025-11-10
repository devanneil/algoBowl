import numpy as np
import random
import time
from inputGenerator import createInput, visualize
from outputVerification import takeColor, zeroOutMoves, condense, readInput, readOutput 

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

# Test imports and basic functionality
if __name__ == "__main__":
    inputArray = createInput(100, 100, random.randint(1,100))
    move = (random.randint(1,10), random.randint(1,10))
    print(inputArray)
    startTime = time.perf_counter()
    print("Taking move: ", move)
    count, takeSet = takeColor(inputArray, move[0], move[1])
    print(takeSet)
    takeTime = time.perf_counter()
    condense(inputArray, takeSet)
    print("After take: ")
    print(inputArray)
    condenseTime = time.perf_counter()
    visualize(inputArray)
    print("Total time: ", condenseTime - startTime)
