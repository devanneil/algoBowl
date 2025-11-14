import numpy as np
import networkx as nx
from models import createInput
from decisionLogic import heuristic, generateSuccessors
from outputVerification import fullOutputCheck
import time
import multiprocessing as mp
import hashlib

def state_hash(state: np.ndarray):
    return hashlib.sha256(state.astype(np.int8).tobytes()).hexdigest()

'''
decisionTree will make fucniton calls to decisionLogic and will handle the networkX graph
'''
finalStates = set()
bestState = None
bestScore = 0
def evaluate_successor(args):
    """Runs heuristic + scoring for a successor (for multiprocessing)."""
    state, count, prevScore, x, y, color, takeSet = args
    score = (count - 1)**2 + prevScore
    heuristicValue = heuristic(state)
    index = state_hash(state)

    return (index, state, count, score, heuristicValue, x, y, color, takeSet)

def buildTree(graph: nx.Graph, rootState: np.ndarray, prevScore: int, maxDepth: int, maxChildren: int, pool, alpha=0):
    #print("Layer:", maxDepth)
    global bestScore, bestState, finalStates

    successorStates = generateSuccessors(rootState, 4*maxChildren)
    rootIndex = state_hash(rootState)

    # Prepare arguments for multiprocessing
    task_args = [(state, count, prevScore, x, y, color, takeSet)
                 for count, state, x, y, color, takeSet in successorStates]

    # Use a process pool to evaluate successors in parallel
    results = pool.map(evaluate_successor, task_args)

    children = []
    for index, state, count, score, heuristicValue, x, y, color, takeSet in results:
        if count <= 1:
            continue
        if score + heuristicValue <= alpha:
            continue
        if index in graph.nodes:
            if graph.nodes[index]["score"] < score:
                graph.nodes[index]["score"] = score
                graph.remove_edge(graph.nodes[index]["parent"], index)
                heuristicValue = graph.nodes[index]["heuristicValue"]
            continue

        finish = (maxDepth == 0)
        if finish:
            finalStates.add(index)
        if score > bestScore:
            bestScore = score
            bestState = state
            alpha = bestScore
            print("New best:", bestScore)

        graph.add_node(index, state=state, score=score, count = count, heuristicValue=heuristicValue, finish=finish, parent=rootIndex)
        graph.add_edge(rootIndex, index, move=(x, y), count=count, color=color, colorSet=takeSet)
        if not finish:
            children.append((state, heuristicValue, score))
    if len(children) == 0: return
    # Recurse on top children
    sorted_children = sorted(children, key=lambda x: x[1], reverse=True)
    next_children = sorted_children[:maxChildren]
    for state, _, score in next_children:
        buildTree(graph, state, score, maxDepth - 1, maxChildren, pool, alpha)

def traceBack(graph: nx.Graph, goal: np.ndarray):
    if goal is None:
        return [], 0
    current = state_hash(goal)
    outputList = []
    count = 0
    while current is not None:
        parent = graph.nodes[current]["parent"]
        if parent is None:
            break
        edge = graph.edges[(parent, current)]
        takeX = (edge['move'][0])
        takeY = edge['move'][1]
        outputList.append((int(edge["color"]), edge["count"], takeX, takeY))
        current = parent
        count += 1
    outputList.reverse()
    return outputList, count
        
def expandAndSearch(decisionTree: nx.graph, inputArray: np.ndarray, maxDepth: int, maxChildren: int, stateScore = 0):
    if inputArray is None:
        return 0, None
    decisionTree.add_node((state_hash(inputArray)), state=inputArray, score=0, heuristicValue = 0, finish=False, parent=None)
    with mp.Pool(processes=min(mp.cpu_count(), 4)) as pool:
        buildTree(graph=decisionTree, rootState=inputArray, prevScore=stateScore, maxDepth=maxDepth, maxChildren=maxChildren, pool=pool)
    return bestScore, bestState
    
if __name__ == "__main__":
    inputArray = createInput(10,10)
    decisionTree = nx.DiGraph()
    startTime = time.perf_counter()
    expandAndSearch(decisionTree, inputArray, 10, 5)
    finishTime = time.perf_counter()
    print(decisionTree)
    print(finishTime - startTime)
    print(bestScore)
    print(bestState)
    bestIndex = (state_hash(bestState))
    print(decisionTree.nodes[bestIndex]["score"])
    #print(bestIndex)
    

    outputList, count = traceBack(decisionTree, bestState)
    print(count)
    for line in outputList:
        print(line[0], line[1], line[2], line[3])


    print(inputArray[inputArray.shape[0] - outputList[0][2]][[outputList[0][3] - 1]])
    fullOutputCheck(outputList, bestScore, inputArray)
    
