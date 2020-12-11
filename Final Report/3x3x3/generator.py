import numpy as np
import itertools as it
import torch as tr
import one_hot as oh
import random

class Node(object):
    def __init__(self, state, depth = 1, step = 1, score = 0, path = []):
        self.state = state
        self.depth = depth
        self.step = step
        self.score = score
        self.path = path
        self.child_list = None
        _, mtch = oh.cubie_match(state)
        self.match = mtch
        
    def children(self):
        if self.child_list is None: self.make_childrens()
        return self.child_list
    
    def make_childrens(self):
        self.child_list = list()
        h = oh.heuristic(self.state, self.score, self.depth, self.match, self.path)
        for heu in h:
            self.child_list.append(Node(heu[0], self.depth, (self.step - 1), heu[1], heu[4]))
        return self.child_list
        
def scramble(scramble_depth):
    state = oh.initial_state()
    for i in range(scramble_depth):
        state = random.choice([state.rotx(), state.rot2x(), state.roty(), state.rot2y(), state.rotz(), state.rot2z()])
        
    return state;


def make_choice(node):
    minScore = 100000
    minIndex = 0

    bestRank = 0
    rankIndex = 0
    #print("length of list: ", len(node.children()))
    for x in range (len(node.children())):
        #print (node.children()[x].path)
        
        if bestRank < node.children()[x].match:
            bestRank = node.children()[x].match
            rankIndex = x
        if bestRank == node.children()[x].match:
            if node.children()[rankIndex].score > node.children()[x].score:
                rankIndex = x
                #print(node.children()[x].path)
            
    return rankIndex

def generate(scrambe_depth = 5, depth = 1, steps = 1, num_games = 1):
    data = list()
    for game in range(num_games):
        state = scramble(scramble_depth)
        node = Node(state, depth, steps)
        #print("\nScramble")
        #node.state.disp()
        for step in range(steps):
            print("game %d, turn %d"%(game,step))
            
            #generate states
            #node.children()
            
            #add states to data ##
            for child in range(len(node.children())):
                data.append(((node.children()[child].state), (node.children()[child].match)))
            #make choice, the most matched and lowest score one
            i = make_choice(node)
            node = node.children()[i]
            #if solved, ended
            if node.match == 27:
                print("\nSolve")
                print("Path is :")
                print(node.path)
                #node.state.disp()
                break
            #print("\nCurrent best resut is:")
            #node.state.disp()

    return data
            
def get_batch(scramble_depth, depth, steps, num_games):
    data = generate(scramble_depth, depth, steps, num_games)
    length = len(data)
    inputs = tr.zeros([length,3,3,3,3,6])
    outputs = tr.zeros([length, 1])

    for i in range(length):
        a, b = data[i]
        inputs[i] = tr.from_numpy(a.cube)
        outputs[i, 0] = b

    return inputs, outputs

if __name__ == "__main__":
    print("\nPlease input the size of the training data: ")
    scramble_depth = int(input("\nPlease input the scramble_depth: "))
    depth = int(input("\nPlease input the max depth of each step: "))
    steps = int(input("\nPlease input the max steps in a game: "))
    num_games = int(input("\nPlease input the number of the games: "))
    inputs, outputs = get_batch(scramble_depth, depth, steps, num_games)
    
    import pickle as pk
    with open("training_data_%d_scramble_depth.pkl" % scramble_depth, "wb") as f: pk.dump((inputs, outputs), f) 
