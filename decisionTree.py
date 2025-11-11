import numpy as np
import networkx as nx
from models import createInput
from decisionLogic import heuristic, generateSuccessors

'''
decisionTree will make fucniton calls to decisionLogic and will handle the networkX graph
'''
finalStates = set()
bestState = 0
bestScore = 0
def buildTree(graph : nx.Graph, rootState : np.ndarray, prevScore : int, maxDepth : int, maxChildren : int):
    print("Layer: ", maxDepth)
    global bestScore, bestState, finalStates
    successorStates = generateSuccessors(rootState, 100)
    children = []
    rootIndex = rootState.tobytes()
    for count, state, x, y, color in successorStates:
        index = state.tobytes()
        score = (count - 1)**2 + prevScore
        heuristicValue = 0
        if index in graph.nodes:
            if graph.nodes[index]["score"] < score:
                graph.nodes[index]["score"] = score
                graph.remove_edge(graph.nodes[index]["parent"], index)
                heuristicValue = graph.nodes[index]["heuristicValue"]
        else:
            heuristicValue = heuristic(state)
        finish = False
        if(maxDepth == 0):
            finish = True
            finalStates.add(index)
        if score > bestScore:
            bestScore = score
            bestState = state
            print("New best: ", bestScore)
        graph.add_node(index, state=state, score=score, heuristicValue = heuristicValue, finish=finish, parent = rootIndex)
        graph.add_edge(rootIndex, index, move = (x,y), count = count, color = color)
        if not finish:
            children.append((state, heuristicValue, score))
    sorted_children = sorted(children, key=lambda x: x[1], reverse=True)
    next_children = sorted_children[:maxChildren]
    for state, _, score in next_children:
        buildTree(graph, state, score, maxDepth-1, maxChildren)
if __name__ == "__main__":
    inputArray = createInput(100,100)
    decisionTree = nx.DiGraph()
    decisionTree.add_node(inputArray.tobytes(), state=inputArray, score=0, heuristicValue = 0, finish=False, parent=None)
    buildTree(graph=decisionTree, rootState=inputArray, prevScore=0, maxDepth=100, maxChildren=10)
    print(decisionTree)
