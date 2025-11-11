from models import takeColor, zeroOutMoves, condense, createInput
import numpy as np
import random
'''
decisionLogic will handle utility functions 
'''
# Heuristic functions to guess at the game score to decide what decisions to make

# Score based on large groups
def groupHeuristic(state : np.ndarray):
    visited = np.zeros_like(state, dtype=bool)
    total_score = 0

    def dfs(r, c, color):
        stack = [(r, c)]
        size = 0
        while stack:
            x, y = stack.pop()
            if (0 <= x < state.shape[0] and 0 <= y < state.shape[1]
                and not visited[x, y] and state[x, y] == color):
                visited[x, y] = True
                size += 1
                # 4-directional adjacency
                stack.extend([(x+1, y), (x-1, y), (x, y+1), (x, y-1)])
        return size

    for i in range(state.shape[0]):
        for j in range(state.shape[1]):
            if not visited[i, j] and state[i, j] != 0:
                group_size = dfs(i, j, state[i, j])
                # Weighted by size^2 (optional)
                total_score += group_size ** 2

    return total_score

# Score based on color sums
def colorHeuristic(state : np.ndarray):
    return None

# Score based on size
def sizeHeuristic(state : np.ndarray):
    return None

def heuristic(state: np.ndarray):
    return groupHeuristic(state)

# Builds successor states based on current state and returns the children states
def generateSuccessors(state: np.ndarray, numSuccessors: int):
    maxX, maxY = state.shape
    evals = set()
    for i in range(numSuccessors):
        x = random.randint(1, maxX)
        y = random.randint(1, maxY)
        if (x,y) not in evals:
            evals.add((x,y))
    successors = []
    for (x,y) in evals:
        successorState = state.copy()
        count, takeSet, color = takeColor(successorState, x, y)
        if count != 0:
            condense(successorState, takeSet)
            successors.append((count, successorState, x, y, color))
    return successors

if __name__ == "__main__":
    width = 100
    height = 100
    print("Creating and testing input of size: ", width, height)
    colors = createInput(width, height, random.randint(0,10))
    successorStates = generateSuccessors(colors, min(colors.shape[0]*colors.shape[1], 100))
    for count, state, x, y, color in successorStates:
        print(x, y, count, heuristic(state))