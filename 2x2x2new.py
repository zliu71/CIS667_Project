import numpy as np
import itertools as it
import matplotlib.pyplot as pt

#colors
N, R, G, B ,W, Y, O = range(7)

class RubiksState(object):
    def __init__(self):
        self.cube = np.zeros((2,2,2,3), dtype = int)

    def actions(self, action):
        new_state = initial_state()

    def rotx(self):
        state = initial_state()
        state.cube[:,:,:,:] = self.cube[:,:,:,:]
        state.cube[0,:,:] = np.rot90(self.cube[0,:,:])
        return state

    def roty(self):
        state = initial_state()
        state.cube[:,:,:,:] = self.cube[:,:,:,:]
        state.cube[:,0,:] = np.rot90(self.cube[:,0,:])
        return state

    def rotz(self):
        state = initial_state()
        state.cube[:,:,:,:] = self.cube[:,:,:,:]
        state.cube[:,:,0] = np.rot90(self.cube[:,:,0])
        return state
    
        """
    def rotx(self):
        state = initial_state()
        #red rotate
        state.cube[0,:,:,0] = np.rot90(self.cube[0,:,:,0],1)
        #shift blue to white
        state.cube[:,0,0,1] = (self.cube[:,0,0,2])
        #shift yellow to blue
        state.cube[:,0,0,2] = (self.cube[:,1,0,1])
        #shift green to yellow
        state.cube[:,1,0,1] = (self.cube[:,0,1,2])
        #shift white to green
        state.cube[:,0,1,2] = (self.cube[:,0,0,1])
        return state

    def roty(self):
        state = initial_state()
        #yellow rotate
        state.cube[:,1,:,1] = np.rot90(self.cube[:,1,:,1],1)
        #orange to blue
        state.cube[1,:,0,2] = (self.cube[1,:,1,0])
        #green to orange
        state.cube[1,:,1,0] = (self.cube[1,:,1,2])
        #red to green
        state.cube[1,:,1,2] = (self.cube[1,1,:,0])
        #blue to red
    
def rotx(disp):
    new_state = np.zeros((6,8),dtype = int)
    new_state[:,:] = disp[:,:] 
    new_state[0:2,2] = disp[2:4,2]
    new_state[2:4,2] = disp[4:6,2]
    #green(backside) -> yellow
    new_state[4:6,2] = np.flip(disp[2:4,7])
    #white -> green(backside)
    new_state[2:4,7] = np.flip(disp[0:2,2])
    #red
    new_state[2:4,0:2] = np.rot90(disp[2:4,0:2])
    return convert(new_state)

    

def roty(disp):
    new_state = np.zeros((6,8),dtype = int)
    new_state[:,:] = disp[:,:]
    new_state[3,2:8] = disp[3,0:6]
    new_state[3,0:2] = disp[3,6:8]
    #yellow
    new_state[4:6,2:4] = np.rot90(np.rot90(np.rot90(disp[4:6,2:4])))
    return convert(new_state)
    
    
    
def rotz(disp):
    new_state = np.zeros((6,8),dtype = int)
    new_state[:,:] = disp[:,:]
    #blue
    new_state[2:4,2:4] = np.rot90(np.rot90(np.rot90(disp[2:4,2:4])))
    #red
    new_state[2:4,1] = disp[4,2:4]
    #red -> white
    new_state[1,2:4] = np.flip(disp[2:4,1])
    #orange
    new_state[2:4,4] = disp[1,2:4]
    #blue -> yellow
    new_state[4,2:4] = np.flip(disp[2:4,4])
    return convert(new_state)
    """
def initial_state():
    state = RubiksState()
    state.cube[0,:,:,0] = R
    state.cube[1,:,:,0] = O
    state.cube[:,0,:,1] = W
    state.cube[:,1,:,1] = Y
    state.cube[:,:,1,2] = G
    state.cube[:,:,0,2] = B
    return state

def cubie_match(state):
    rtvalue = []
    match = 0
    
    for i,j,k in it.product([0,1],repeat = 3):
        #return matched cubies
        if(np.all(state.cube[i,j,k,:] == initial_state().cube[i,j,k,:])):
            #print(state.cube[i,j,k])
            #print(initial_state().cube[i,j,k])
            #rtvalue.append((i,j,k))
            match = match + 1
        #return unmatched cubies
        else :
            rtvalue.append((i,j,k))
    #print (match)
    return rtvalue, match
#A* is a bfs search for searching heuristic 
def A_star_solve(state, threshold, step): 
    cubies, match = cubie_match(state)
    score = 0
    steps = step
    path = []
    for c in range(threshold):
        h = np.array(heuristic(state, score, steps, match, path))
        idx = search_result(h)
        state = h[idx, 0]
        score = h[idx, 1]
        match = h[idx, 3]
        steps = step
        path = h[idx, 4]
        print ("Match is")
        print (match)
        print ("Score is")
        print (score)
        
        if(match == 8):
            print ("Path is")
            print (path)
            print ("Score is")
            print (score)
            print ("Current state")
            print (state.cube)
            return True
        
    #check if any cubie match, get score
    #pick an unmatch cubie, dfs until match
    #compare results, find the best one
    print("Cannot find a solve in current state")
    print ("Path is")
    print (path)
    print ("Score is")
    print (score)
    print ("Current state")
    print (state.cube)
    return False
#number of steps, matched cubies, costs


#dfs in n steps to find the heuristic and the score
def heuristic(state, score, steps, match, path):
    if(match == 8):
        return [[state, score, steps, match, path]]
    if(steps == 0):
        _, mtch = cubie_match(state);
        if(mtch >= match):
            return [[state, score, 0, mtch, path]]
        return []

    h = []
    flag = 0
    for child in [state.rotx(),state.roty(),state.rotz()]:
        path_temp = path.copy()
        path_temp.append(index_to_path(flag))
        _, mtch = cubie_match(child)
        h_temp = heuristic(child, (score + (8 - mtch)), (steps - 1), mtch, path_temp) 
        flag = flag + 1
        if(h_temp != []):
            h.extend(h_temp)
        #print ("label1")
    return h

def index_to_path(index):
    if index == 0:
        return "x"
    if index == 1:
        return "y"
    if index == 2:
        return "z"

def search_result(arr):
    #if sloved, find best result
    minScore = 100000
    minIndex = 0

    bestRank = 0
    rankIndex = 0
    print("sizeof")
    print(arr[:,0].size)
    for x in range (arr[:,3].size):
        #print (arr[x,:])
        if bestRank < arr[x,3]:
            bestRank = arr[x,3]
            rankIndex = x
            #print (arr[x,1])
        
    return rankIndex
def random_process(state, step): 
    cubies, match = cubie_match(state)
    score = 0
    steps = step
    path = []
    h = np.array(heuristic(state, score, steps, match, path))
    idx = search_result(h)
    state = h[idx, 0]
    score = h[idx, 1]
    match = h[idx, 3]
    steps = step
    path = h[idx, 4]
    if(match == 8):
        print ("Solve success!")
        print ("Path is")
        print (path)
        print ("Score is")
        print (score)
        print ("Current state")
        print (state.cube)
        return True
        
    print("Cannot find a solve in current state")
    print ("Path is")
    print (path)
    print ("Score is")
    print (score)
    print ("Current state")
    print (state.cube)
    return False


"""
def slove(state, heuristic):
    return True
def display(state):
    disp = np.zeros((6,8),dtype = int)
    disp[2:4,0:2] = state.cube[0,:,:,0] #r = 1
    disp[2:4,4:6] = state.cube[1,:,:,0] #o = 6
    disp[0:2,2:4] = state.cube[:,0,:,1] #w = 4
    disp[4:6,2:4] = state.cube[:,1,:,1] #y = 5
    disp[2:4,6:8] = state.cube[:,:,1,2] #g = 2
    disp[2:4,2:4] = state.cube[:,:,0,2] #b = 3
    print (disp)
    return disp
def convert(disp):
    state = initial_state()
    state.cube[0,:,:,0] = disp[2:4,0:2]
    state.cube[1,:,:,0] = disp[2:4,4:6]
    state.cube[:,0,:,1] = disp[0:2,2:4]
    state.cube[:,1,:,1] = disp[4:6,2:4]
    state.cube[:,:,1,2] = disp[2:4,6:8]
    state.cube[:,:,0,2] = disp[2:4,2:4]
    return state
"""


if __name__ == "__main__":
    state = initial_state()
    print("Tutorial:\nThis demo has two functions, \n#1 is solve the cube by A* algorithm,\n#2 is solve the cube by random_process.\nBefore solve the cube, you need to manually scramble the rubik cube and give the maximun step\nwhich is how far the heuristic should go: more step, more accurace, much slower\nless step, less accuate, much faster,\nhint: do not make it too complex, do not give a redicicously huge max step (more than 10).\nAfterthat you need to setup the threshhold, \nwhich is the maximun step that A* algorithm trying to find the result\nIn other words: max step is accuracy of the heuristic, threshold is the accuracy of A* algorithm.")
    print("\n\nStep one: manually scramble the rubik cube, do not make it too complex\n")
    while True:
        
        print("Current state:")
        print(state.cube)
        a = input("Enter an action ('x'=rotx,'y'=roty, 'z'=rotz, 'q'=quit): ")
        if a == "x": state = state.rotx()
        if a == "y": state = state.roty()
        if a == "z": state = state.rotz()
        if a == "q": break
    #state = state.rotx().roty().rotz().rotz().roty().rotx().roty().rotz().rotx().roty()
    #state = state.rotx().roty().rotz()
    backup = initial_state()
    backup.cube[:,:,:,:] = state.cube[:,:,:,:]
    print("\nStep two: input the max 'steps' to solve: ")
    maxDepth = int(input())
    print("Step three: input the 'threshold' to slove: ")
    threshold = int(input())
    """
    #a = (heuristic(rotz(display(state)), 0, 5, 0, 4))
    #print (a)
    #print(state.cube)
    a = state.rotx()
    #display(a)
    print(a.cube)

    ht = np.array(heuristic(a, 0, 3, 0, []))
    idx = search_result(ht)
    print (ht)
    print(ht[:,0].size)
    print(idx)
    print(ht[idx,3])
    #search_result(ht)
    #cubie_match(a.rotx())
    #a = display(roty(display(rotx(display(state)))))
    #display(rotz(display(rotx(a))))
    #print(rotz(display(rotx(a))).cube[0,:,:])
    #display(state.rotx())
    """
    test = A_star_solve(state, threshold, maxDepth)
    if (test == True):
        print("A* algorithm solve success!")
    if (test == False):
        print("A* algorithm slove failed! probably need more 'step' to find a formula:\ntry some long steps like 10 - 12 steps, might be really slow but works fine!")
    print("\nRandom process, please provide a valid steps\nthat random process function can be executed.")
    max_steps = int(input("Enter steps: "))
    result = random_process(backup, max_steps)
    
    
    
    
    
