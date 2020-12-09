import numpy as np
import itertools as it

class RubiksState(object):
    def __init__(self):
        self.cube = np.zeros((2,2,2,3,6), dtype = int)

    def actions(self, action):
        new_state = initial_state()

    def rotx(self):
        state = initial_state()
        state.cube[:,:,:,:,:] = self.cube[:,:,:,:,:]
        #print(self.cube[0,:,:])
        state.cube[0,:,:] = np.rot90(self.cube[0,:,:])
        buf = np.zeros((2,2,6),int)
        buf[:,:,:] = state.cube[0,:,:,1,:]
        state.cube[0,:,:,1,:] = state.cube[0,:,:,2,:]
        state.cube[0,:,:,2,:] = buf
        #print(state.cube[0,:,:])
        return state

    def rot2x(self):
        return self.rotx().rotx()
        """
        state = initial_state()
        state.cube[:,:,:,:,:] = self.cube[:,:,:,:,:]
        state.cube[0,:,:] = np.rot90(self.cube[0,:,:],2)
        buf = np.zeros((2,2,6),int)
        buf[:,:,:] = state.cube[0,:,:,1,:]
        state.cube[0,:,:,1,:] = state.cube[0,:,:,2,:]
        state.cube[0,:,:,2,:] = buf
        return state
        return state
        
    
    def rotxp(self):
        state = initial_state()
        state.cube[:,:,:,:,:] = self.cube[:,:,:,:,:]
        state.cube[0,:,:] = np.rot90(self.cube[0,:,:],3)
        buf = np.zeros((2,2,6),int)
        buf[:,:,:] = state.cube[0,:,:,1,:]
        state.cube[0,:,:,1,:] = state.cube[0,:,:,2,:]
        state.cube[0,:,:,2,:] = buf
        return state
        return state
        """
    
    def roty(self):
        state = initial_state()
        state.cube[:,:,:,:,:] = self.cube[:,:,:,:,:]
        state.cube[:,0,:] = np.rot90(state.cube[:,0,:])
        buf = np.zeros((2,2,6),int)
        buf[:,:,:] = state.cube[:,0,:,2,:]
        state.cube[:,0,:,2,:] = state.cube[:,0,:,0,:]
        state.cube[:,0,:,0,:] = buf
        return state

    def rot2y(self):
        return self.roty().roty()
        """
        state = initial_state()
        state.cube[:,:,:,:,:] = self.cube[:,:,:,:,:]
        state.cube[:,0,:] = np.rot90(state.cube[:,0,:],2)
        buf = np.zeros((2,2,6),int)
        buf[:,:,:] = state.cube[:,0,:,2,:]
        state.cube[:,0,:,2,:] = state.cube[:,0,:,0,:]
        state.cube[:,0,:,0,:] = buf
        return state
        
    def rotyp(self):
        state = initial_state()
        state.cube[:,:,:,:,:] = self.cube[:,:,:,:,:]
        state.cube[:,0,:] = np.rot90(state.cube[:,0,:],3)
        buf = np.zeros((2,2,6),int)
        buf[:,:,:] = state.cube[:,0,:,2,:]
        state.cube[:,0,:,2,:] = state.cube[:,0,:,0,:]
        state.cube[:,0,:,0,:] = buf
        return state
        """

    def rotz(self):
        state = initial_state()
        state.cube[:,:,:,:,:] = self.cube[:,:,:,:,:]
        state.cube[:,:,0] = np.rot90(state.cube[:,:,0])
        buf = np.zeros((2,2,6),int)
        buf[:,:,:] = state.cube[:,:,0,0,:]
        state.cube[:,:,0,0,:] = state.cube[:,:,0,1,:]
        state.cube[:,:,0,1,:] = buf
        return state

    def rot2z(self):
        return self.rotz().rotz()
        """
        state = initial_state()
        state.cube[:,:,:,:,:] = self.cube[:,:,:,:,:]
        state.cube[:,:,0] = np.rot90(state.cube[:,:,0],2)
        return state
        
    def rotzp(self):
        state = initial_state()
        state.cube[:,:,:,:,:] = self.cube[:,:,:,:,:]
        state.cube[:,:,0] = np.rot90(state.cube[:,:,0],3)
        return state
        """

    
    
    def disp(self):
        print("\nup")
        print(self.cube[:,1,:,1])
        print("\ndown")
        print(self.cube[:,0,:,1])
        print("\nfront")
        print(self.cube[:,:,0,2])
        print("\nback")
        print(self.cube[:,:,1,2])
        print("\nleft")
        print(self.cube[1,:,:,0])
        print("\nright")
        print(self.cube[0,:,:,0])

    

def initial_state():
    state = RubiksState()
    state.cube[0,:,:,0,0] = 1 #R
    state.cube[1,:,:,0,1] = 1 #O
    state.cube[:,0,:,1,2] = 1 #W
    state.cube[:,1,:,1,3] = 1 #Y
    state.cube[:,:,1,2,4] = 1 #G
    state.cube[:,:,0,2,5] = 1 #B
    return state

def cubie_match(state):
    rtvalue = []
    match = 0
    
    for i,j,k in it.product([0,1],repeat = 3):
        #return matched cubies
        if(np.all(state.cube[i,j,k,:,:] == initial_state().cube[i,j,k,:,:])):
            #print(state.cube[i,j,k])
            #print(initial_state().cube[i,j,k])
            #rtvalue.append((i,j,k))
            match = match + 1
        #return unmatched cubies
        else :
            rtvalue.append((i,j,k))
    #print (match)
    return rtvalue, match
#A* is a search picking heuristic 
def A_star_solve(state, step, dpth): 
    cubies, match = cubie_match(state)
    score = 0
    depth = dpth
    path = []
    for c in range(step):
        h = np.array(heuristic(state, score, depth, match, path))
        idx = search_result(h)
        state = h[idx, 0]
        score = h[idx, 1]
        match = h[idx, 3]
        depth = dpth
        path = h[idx, 4]
        print ("Match is")
        print (match)
        print ("Path is")
        print (path)
        print ("Score is")
        print (score)
        print ("Current state")
        state.disp()
        if(match == 8):
            return True
        hold = input("press enter to the next turn")
    print("Cannot find a solve in current state")
    return False


#dfs in n steps to find the heuristic and the score
def heuristic(state, score, depth, match, path):
    #print(match)
    #print(path)
    if(match == 8):
        return [[state, score, depth, match, path]]
    if(depth == 0):
        _, mtch = cubie_match(state);
        if(mtch >= match):
            return [[state, score, 0, mtch, path]]
        return []

    h = []
    flag = 0
    for child in [state.rotx(), state.rot2x(), state.roty(), state.rot2y(), state.rotz(), state.rot2z()]:
    #for child in [state.rotx(), state.rot2x(), state.rotxp(), state.roty(), state.rot2y(), state.rotyp(), state.rotz(), state.rot2z(), state.rotzp()]:
        path_temp = path.copy()
        path_temp.append(index_to_path(flag))
        _, mtch = cubie_match(child)
        h_temp = heuristic(child, (score + (8 - mtch)), (depth - 1), mtch, path_temp) 
        flag = flag + 1
        if(h_temp != []):
            h.extend(h_temp)
        #print ("label1")
    return h

def index_to_path(index):
    if index == 0:
        return "x"
    if index == 1:
        return "2x"
    if index == 2:
        return "y"
    if index == 3:
        return "2y"
    if index == 4:
        return "z"
    if index == 5:
        return "2z"
   
    """
    if index == 0:
        return "x"
    if index == 1:
        return "2x"
    if index == 2:
        return "xp"
    if index == 3:
        return "y"
    if index == 4:
        return "2y"
    if index == 5:
        return "yp"
    if index == 6:
        return "z"
    if index == 7:
        return "2z"
    if index == 8:
        return "zp"
    """
def search_result(arr):
    #if sloved, find best result
    minScore = 100000
    minIndex = 0

    bestRank = 0
    rankIndex = 0
    print("sizeof")
    print(arr.size)
    for x in range (arr.size):
        #print (arr[x,:])
        if bestRank < arr[x,3]:
            bestRank = arr[x,3]
            rankIndex = x
        if bestRank == arr[x,3]:
            #print(arr[rankIndex,1])
            #print(arr[x,1])
            if arr[rankIndex,1] > arr[x,1]:
                #print(x)
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
        #print (state.cube)
        state.disp()
        return True
        
    print("Cannot find a solve in current state")
    print ("Path is")
    print (path)
    print ("Score is")
    print (score)
    print ("Current state")
    state.disp()
    return False


if __name__ == "__main__":
    state = initial_state()
    print("Tutorial:\nThis demo has two functions, \n#1 is solve the cube by A* algorithm,\n#2 is solve the cube by random_process.\nBefore solve the cube, you need to manually scramble the rubik cube and give the maximun step\nwhich is how far the heuristic should go: more step, more accurace, much slower\nless step, less accuate, much faster,\nhint: do not make it too complex, do not give a redicicously huge max step (more than 10).\nAfterthat you need to setup the threshhold, \nwhich is the maximun step that A* algorithm trying to find the result\nIn other words: max step is accuracy of the heuristic, threshold is the accuracy of A* algorithm.")
    print("\n\nStep one: manually scramble the rubik cube, do not make it too complex\n")
    while True:
        
        print("Current state:")
        state.disp()
        a = input("Enter an action ('x'=rotx,'y'=roty, 'z'=rotz, 'q'=quit): ")
        if a == "x": state = state.rotx()
        if a == "y": state = state.roty()
        if a == "z": state = state.rotz()
        if a == "q": break
    #state = state.rotx().roty().rotz().rotz().roty().rotx().roty().rotz().rotx().roty()
    #state = state.rotx().roty().rotz()
    backup = initial_state()
    backup.cube[:,:,:,:] = state.cube[:,:,:,:]
    print("\nStep two: input the max 'depth' to solve: ")
    maxDepth = int(input())
    print("Step three: input the 'steps' to slove: ")
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
    
    
    
    
    
