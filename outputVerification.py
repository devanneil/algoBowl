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
        return (0, None, 0)
    
    stack = [(realX, realY)]
    takeSet = set()
    visited = set()
    count = 0
    while stack:
        cx, cy = stack.pop()
        visited.add((cx, cy))
        if input[cx][cy] == target:
            takeSet.add((cx, cy))
            count += 1

        # check cardinal neighbors
        for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:
            nx, ny = cx + dx, cy + dy
            if 0 <= nx < shape[0] and 0 <= ny < shape[1] and input[nx, ny] == target and (nx, ny) not in visited:
                stack.append((nx, ny))

    return count, takeSet, target

def zeroOutMoves(input: np.ndarray, moveList: list):
    for (x,y) in moveList:
        input[x][y] = 0

def condense(arr : np.ndarray, colorSet: list):
    zeroOutMoves(arr, colorSet)
    affected_cols = {y for _, y in colorSet}
    affected_rows = {x for x, _ in colorSet}

    n_rows, n_cols = arr.shape

    for col in affected_cols:
        # Extract the column
        column = arr[:, col]
        # Get all non-zero elements
        nonzeros = column[column != 0]
        # Fill the bottom part of the column with non-zeros
        arr[:, col] = 0
        arr[n_rows - len(nonzeros):, col] = nonzeros

    for row in affected_rows:
        line = arr[row, :]
        nonzeros = line[line != 0]
        arr[row, :] = 0
        arr[row, :len(nonzeros)] = nonzeros

def readInput(fname : str):
    with open(fname, "r") as inputFile:
        n, m = map(int, inputFile.readline().strip().split())
        colors = np.zeros((n,m), dtype=int)
        for i in range(n):
            line = list(inputFile.readline())
            for j in range(m):
                colors[i][j] = int(line[j])
    return colors

def readOutput(oname : str):
    with open(oname, "r") as inputFile:
        scorePred = int(inputFile.readline())
        moves = int(inputFile.readline())
        moveList = []
        for i in range(moves):
            color, pairs, x, y = map(int, inputFile.readline().split())
            moveList.append((color, pairs, x, y))
            
    return moveList, scorePred

def fullOutputCheck(moveList: list, scorePred: int, colorsArray: np.ndarray):
    #moveList Structure, (color, count, takeX, takeY)
    score = 0
    for move in moveList:
        takeX = move[2]
        takeY = move[3]
        print(takeX, takeY)
        shape = colorsArray.shape
        realX = int(shape[0]) - takeX
        realY = takeY - 1
        print(move[0])
        print(realX, realY)
        if colorsArray[realX][realY] != move[0]:
            print("INVALID MOVE!! Wrong Color")
            print(move)
            print(colorsArray[realX][realY])
            break
        count, takeSet, color = takeColor(colorsArray, takeX, takeY)
        if count != move[1]:
            print("INVALID MOVE!! Wrong count")
            print(move)
            print(count)
            break
        if (realX, realY) not in takeSet:
            print("INVALID MOVE!! Wrong take set")
            print(move)
            print(takeSet)
            break
        score += (count - 1)**2
        condense(colorsArray, takeSet)
    if score != scorePred:
        print("INVALID SCORE!!")
        print(score)

if __name__ == "__main__":
    fname = "input.txt"
    colors = readInput(fname)
    print(colors)
    
    # Create Output reader function, unsure what parts will need
    oname = "outputIn.txt"
    moveList, scorePred = readOutput(oname)

    fullOutputCheck(moveList, scorePred, colors)

    
    