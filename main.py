from decisionTree import traceBack, expandAndSearch
from outputVerification import condense, takeColor
import decisionTree
import networkx as nx
import numpy as np
import glob
import os
import re
from models import readInput, readOutput
import sys
'''
Main will be where we handle inputting the problem, calling the search function, and printing the final result
'''
def fileOutputCheck(moveList: list, scorePred: int, colorsArray: np.ndarray, fname: str):
    #moveList Structure, (color, count, takeX, takeY)
    with open(fname, "w") as outputFile:
        score = 0
        for move in moveList:
            takeX = move[2]
            takeY = move[3]
            outputFile.write("{takeX}, {takeY}\n")
            shape = colorsArray.shape
            realX = shape[0] - takeX
            realY = takeY - 1
            outputFile.write("{move[0]}\n")
            outputFile.write("{realX}, {realY}\n")
            if colorsArray[realX][realY] != move[0]:
                outputFile.write("INVALID MOVE!! Wrong Color")
                outputFile.write("{move}")
                outputFile.write("{colorsArray[realX][realY]}")
                break
            count, takeSet, color = takeColor(colorsArray, takeX, takeY)
            if count != move[1]:
                outputFile.write("INVALID MOVE!! Wrong count")
                outputFile.write("{move}")
                outputFile.write("{count}")
                break
            if (realX, realY) not in takeSet:
                outputFile.write("INVALID MOVE!! Wrong take set")
                outputFile.write("{move}")
                outputFile.write("{takeSet}")
                break
            score += (count - 1)**2
            condense(colorsArray, takeSet)
        if score != scorePred:
            outputFile.write("INVALID SCORE!!")
            outputFile.write("{score}")

if __name__ == "__main__":
    folder_path = "all_inputs/inputs"
    files = sys.argv[1:]
    if len(files) == 0:
        print("Must provide a file!")

    for path in files:
        decisionTree.bestState = None
        decisionTree.bestScore = 0
        filename = os.path.basename(path)
        # Extract digits after "input_group"
        match = re.search(r"input_group(\d+)\.txt$", filename)
        if not match:
            continue  # skip unexpected names
        group_number = int(match.group(1))
        print("Evaluating: ", group_number)
        #Evaluate inputs here
        inputArray = readInput(path)
        outputList = []
        count = 0
        currentArray = inputArray
        groupState = None
        groupBest = 0
        for i in range(int(inputArray.shape[0] / 5)):
            evalGraph = nx.DiGraph()
            groupBest, groupState = expandAndSearch(evalGraph, currentArray, 5, 5,  groupBest)
            results = traceBack(evalGraph, groupState)
            count += results[1]
            outputList.extend(results[0])
            currentArray = groupState
            print("Next set: ", i + 1)

        
        output_dir = "./all_outputs"
        os.makedirs(output_dir, exist_ok=True)  # creates folder if it doesn't exist
        oname = "output_group" + str(group_number) + ".txt"

        filePath = os.path.join(output_dir, oname)
        with open(filePath, "w") as outputFile:
            outputFile.write(f"{groupBest}\n")
            outputFile.write(f"{count}\n")
            for line in outputList:
                outputFile.write(f"{line[0]} {line[1]} {line[2]} {line[3]}\n")

        output_dir = "./output_status"
        os.makedirs(output_dir, exist_ok=True)  # creates folder if it doesn't exist
        oname = "output_status" + str(group_number) + ".txt"

        filePath = os.path.join(output_dir, oname)
        fileOutputCheck(outputList, groupBest, inputArray, filePath)

            

