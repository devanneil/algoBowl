from models import takeColor, zeroOutMoves, condense, createInput
import numpy as np
import random
'''
decisionLogic will handle utility functions 
'''
# Heuristic functions to guess at the game score to decide what decisions to make
import numpy as np

def conv2d_numpy(arr, kernel):
    kh, kw = kernel.shape
    ah, aw = arr.shape
    pad_h, pad_w = kh // 2, kw // 2

    # Zero-pad
    padded = np.pad(arr, ((pad_h, pad_h), (pad_w, pad_w)), mode='constant')

    # Output array
    out = np.zeros_like(arr, dtype=float)

    # Slide window
    for i in range(ah):
        for j in range(aw):
            region = padded[i:i+kh, j:j+kw]
            out[i, j] = np.sum(region * kernel)
    return out
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

def groupHeuristicConv(state: np.ndarray):
    from scipy.signal import convolve2d
    kernel = np.ones((3, 3), dtype=float)
    colors = np.unique(state)
    colors = colors[colors != 0]
    # Stack masks for all colors: shape (num_colors, H, W)
    masks = np.stack([(state == c).astype(float) for c in colors])
    # Apply convolution for each mask
    convs = np.array([convolve2d(m, kernel, mode='same', boundary='fill', fillvalue=0) for m in masks])
    # Compute score per color
    return np.sum(convs * masks)

# Score based on color sums
def colorHeuristic(state : np.ndarray):
    return None

# Score based on size
def sizeHeuristic(state : np.ndarray):
    return None

def heuristic(state: np.ndarray):
    return groupHeuristicConv(state)

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
            successors.append((count, successorState, x, y, color, takeSet))
    return successors

if __name__ == "__main__":
    width = 100
    height = 100
    print("Creating and testing input of size: ", width, height)
    colors = createInput(width, height, random.randint(0,10))
    successorStates = generateSuccessors(colors, min(colors.shape[0]*colors.shape[1], 100))
    for count, state, x, y, color in successorStates:
        print(x, y, count, heuristic(state))