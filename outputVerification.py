'''
This is where we'll be able to verify inputs and outputs
'''
import numpy as np

def takeColor(input : np.ndarray, x : int, y : int):
    shape = input.shape
    realX = int(shape[0]) - x
    realY = y - 1
    target = input[realX][realY]
    if target == 0:
        return 0
    
    stack = [(realX, realY)]
    count = 0
    while stack:
        cx, cy = stack.pop()
        if input[cx][cy] == target:
            input[cx][cy] = 0
            count += 1

        # check cardinal neighbors
        for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:
            nx, ny = cx + dx, cy + dy
            if 0 <= nx < shape[0] and 0 <= ny < shape[1] and input[nx, ny] == target:
                stack.append((nx, ny))

    return count

def condense(arr : np.ndarray):
    n_rows, n_cols = arr.shape

    # Find non-empty columns
    non_empty_cols = np.any(arr != 0, axis=0)
    
    # Count of non-empty columns
    num_non_empty = np.sum(non_empty_cols)
    
    # Shift non-empty columns to the left
    if num_non_empty > 0:
        arr[:, :num_non_empty] = arr[:, non_empty_cols]
    
    # Fill remaining columns with zeros
    if num_non_empty < n_cols:
        arr[:, num_non_empty:] = 0
        
    for j in range(n_cols):
        col = arr[:, j]
        non_zero = col[col != 0]
        num_zeros = n_rows - len(non_zero)
        # Fill top with zeros
        col[:num_zeros] = 0
        # Fill bottom with non-zero values
        col[num_zeros:] = non_zero
    

def zeroOutMoves(input: np.ndarray, moveList: list):
    print(moveList)
    shape = input.shape
    for (x,y) in moveList:
        realX = int(shape[0]) - x
        realY = y - 1
        input[realX][realY] = 0




if __name__ == "__main__":
    fname = "input.txt"
    with open(fname, "r") as inputFile:
        n, m = map(int, inputFile.readline().strip().split())
        colors = np.zeros((n,m), dtype=int)
        for i in range(n):
            line = list(inputFile.readline())
            for j in range(m):
                colors[i][j] = int(line[j])
        print(colors)
    
    oname = "outputIn.txt"
    with open(oname, "r") as inputFile:
        scorePred = int(inputFile.readline())
        moves = int(inputFile.readline())
        moveList = []
        for i in range(moves):
            line = inputFile.readline().split()
            color = int(line[0])
            pairs = int(line[1])
            takeList = []
            for i in range(pairs):
                lineTupple = line[i+2]
                takeList.append(list(map(int, lineTupple.split(','))))
            moveList.append((color, pairs, takeList))

    #moveList Structure, [move][color, number of tiles, list][grid position in list][x, y]
    for move in moveList:
        print(move)
        takeX = move[2][0][0]
        takeY = move[2][0][1]
        print(takeX, takeY)
        simColors = colors.copy()
        zeroOutMoves(simColors, move[2])
        condense(simColors)
        count = takeColor(colors, takeX, takeY)
        condense(colors)
        print(colors)
        print(count)
        print(simColors)
        # If count = 0, invalid move
        # IF simColors != colors, invalid move
    
    