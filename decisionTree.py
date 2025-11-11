import numpy as np
import networkx as nx
from models import createInput
from decisionLogic import heuristic, generateSuccessors

'''
decisionTree will make fucniton calls to decisionLogic and will handle the networkX graph
'''
finalStates = set()
def buildTree(graph : nx.Graph, rootState : np.ndarray, maxDepth : int):
    successorStates = generateSuccessors(rootState, 100)
    for count, state, x, y in successorStates:
        index = state.tobytes()
        score = (count - 1)**2
        if index in graph.nodes:
            if graph.nodes[index]["score"] < score:
                graph.nodes[index]["score"] = score
                graph.remove_edge(graph.nodes[index]["parent"], index)

        heuristicValue = heuristic(state)
        finish = False
        if(maxDepth == 0):
            finish = True
            finalStates.add(index)
        graph.add_node(index, state=state, score=score, heuristicValue = heuristicValue, finish=finish, parent = rootState.tobytes())
        graph.add_edge(rootState.tobytes(), index, move = (x,y), count = count)
if __name__ == "__main__":
    inputArray = createInput(100,100)
    decisionTree = nx.DiGraph()
    decisionTree.add_node(inputArray.tobytes(), state=inputArray, score=0, heuristicValue = 0, finish=False, parent=None)
    buildTree(decisionTree, inputArray, 100)
    print(decisionTree)
