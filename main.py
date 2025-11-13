from decisionTree import traceBack, expandAndSearch, bestScore, bestState
import networkx as nx
import numpy as np
import glob
import os
import re
from models import readInput, readOutput
'''
Main will be where we handle inputting the problem, calling the search function, and printing the final result
'''


if __name__ == "__main__":
    folder_path = "all_inputs/inputs"
    files = glob.glob(os.path.join(folder_path, "input_group*.txt"))

    for path in files:
        bestScore = 0
        bestState = 0
        filename = os.path.basename(path)
        # Extract digits after "input_group"
        match = re.search(r"input_group(\d+)\.txt$", filename)
        if not match:
            continue  # skip unexpected names
        group_number = int(match.group(1))
        #Evaluate inputs here
        inputArray = readInput(path)
        evalGraph = nx.DiGraph()
        expandAndSearch(evalGraph, inputArray, 10, 5)
        groupBest = bestScore
        groupState = bestState
        outputList, count = traceBack(evalGraph, groupState)
        oname = "output_group" + str(group_number) + ".txt"
        with open("/all_outputs/" + oname) as outputFile:
            outputFile.write(groupBest)
            outputFile.write(count)
            for line in outputList:
                outputFile.write(line[0], line[1], line[2], line[3])

