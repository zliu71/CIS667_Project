#Zhiguang Liu
#zliu71@syr.edu
#code#1, function for 2x2x2 cube
import numpy as np

class RubiksState(object):
    def __init__(self):
        self.cube = np.empty((6,8), dtype = int)
        self.cube[0:2, 0:2] = 0
        self.cube[4:6, 0:2] = 0
        self.cube[0:2, 4:8] = 0
        self.cube[4:6, 4:8] = 0 
        
        
    def __str__(self):
        rtn = ""
        for x in range (6):
            rtn += "".join(str(self.cube[x, :]))
            if x != 5:
                rtn += "\n"
        print (type (rtn))
        return rtn

    def rotx(self):
        new_state = RubiksState()
        new_state.cube[:,:] = self.cube[:,:]
        new_state.cube[0:2,2] = self.cube[2:4,2]
        new_state.cube[2:4,2] = self.cube[4:6,2]
        #green(backside) -> yellow
        new_state.cube[4:6,2] = np.flip(self.cube[2:4,7])
        #white -> green(backside)
        new_state.cube[2:4,7] = np.flip(self.cube[0:2,2])
        #red
        new_state.cube[2:4,0:2] = np.rot90(self.cube[2:4,0:2])
        return new_state

    def rot_ax(self):
        new_state = RubiksState()
        new_state.cube[:,:] = self.cube[:,:]
        new_state.cube[2:4,2] = self.cube[0:2,2]
        new_state.cube[4:6,2] = self.cube[2:4,2]
        #green(backside) -> yellow
        new_state.cube[2:4,7] = np.flip(self.cube[4:6,2])
        #white -> green(backside)
        new_state.cube[0:2,2] = np.flip(self.cube[2:4,7])
        #red
        new_state.cube[2:4,0:2] = np.rot90(self.cube[2:4,0:2],k = -1)
        return new_state

    def roty(self):
        new_state = RubiksState()
        new_state.cube[:,:] = self.cube[:,:]
        new_state.cube[3,2:8] = self.cube[3,0:6]
        new_state.cube[3,0:2] = self.cube[3,6:8]
        #yellow
        new_state.cube[4:6,2:4] = np.rot90(np.rot90(np.rot90(self.cube[4:6,2:4])))
        return new_state

    def rot_ay(self):
        new_state = RubiksState()
        new_state.cube[:,:] = self.cube[:,:]
        new_state.cube[3,0:6] = self.cube[3,2:8]
        new_state.cube[3,6:8] = self.cube[3,0:2]
        #yellow
        new_state.cube[4:6,2:4] = np.rot90(self.cube[4:6,2:4])
        return new_state
    
    def rotz(self):
        new_state = RubiksState()
        new_state.cube[:,:] = self.cube[:,:]
        #blue
        new_state.cube[2:4,2:4] = np.rot90(np.rot90(np.rot90(self.cube[2:4,2:4])))
        #red
        new_state.cube[2:4,1] = self.cube[4,2:4]
        #red -> white
        new_state.cube[1,2:4] = np.flip(self.cube[2:4,1])
        #orange
        new_state.cube[2:4,4] = self.cube[1,2:4]
        #blue -> yellow
        new_state.cube[4,2:4] = np.flip(self.cube[2:4,4])
        return new_state
    
    def rot_az(self):
        new_state = RubiksState()
        new_state.cube[:,:] = self.cube[:,:]
        #blue
        new_state.cube[2:4,2:4] = np.rot90(self.cube[2:4,2:4])
        #red
        new_state.cube[4,2:4] = self.cube[2:4,1]
        #red -> white
        new_state.cube[2:4,1] = np.flip(self.cube[1,2:4])
        #orange
        new_state.cube[1,2:4] = self.cube[2:4,4]
        #blue -> yellow
        new_state.cube[2:4,4] = np.flip(self.cube[4,2:4])
        return new_state

def initial_state():
    state = RubiksState()
    state.cube[2:4,0:2] = 1
    state.cube[2:4,2:4] = 2
    state.cube[2:4,4:6] = 3
    state.cube[2:4,6:8] = 4
    state.cube[0:2,2:4] = 5
    state.cube[4:6,2:4] = 6
    return state


def recurse_cubie(state, max_depth, score, path): 
    
    if np.array_equal(state.cube, initial_state().cube):
        #print (str(state))
        return [[score, 0, path, state]]
    
    if max_depth == 0:
        
        return [[score, (np.sum(state.cube==initial_state().cube) - 24), path, state]]
    face_results = []
    flag = 0
    for child in [state.rotx(), state.rot_ax(), state.roty(), state.rot_ay(), state.rotz(), state.rot_az()]:
        temp = path.copy()
        temp.append(index_to_path(flag))
        #flag  = flag + 1
        face_result = recurse_cubie(child, max_depth-1, score+1, temp)
        flag = flag + 1
        #print (face_result)
        face_results.extend(face_result)
    
    return face_results

def slove(state, max_depth):

    path = []
    score = 0
    for n in range(max_depth):
        result = np.array(recurse_cubie(state, n+1, score, path))
        getRank = find_minimun_result(result)
        if getRank[0]:
            return print("\nSuccess")
        #state = result[getRank[1], 3]
        #score = result[getRank[1], 0]
        #path = result[getRank[1], 2]
        #print(str(state))
        #print(result[getRank[1],:])

    score = result[getRank[1], 0]
    path = result[getRank[1], 2]
    print("\nFailed, score is")
    print(score)
    print(", path is ")
    print(path)
    
def find_minimun_result(arr):
    #if sloved, find best result
    minScore = 100000
    minIndex = 0

    bestRank = 0
    rankIndex = 0
    print("sizeof")
    print(arr[:,0].size)
    for x in range (arr[:,0].size):
        #print (arr[x,:])
        if (arr[x,1] != 0):
            if bestRank < arr[x,1]:
                bestRank = arr[x,1]
                rankIndex = x
                #print (arr[x,1])
        if (arr[x,1] == 0):
            if minScore > arr[x,0]:
                minScore = arr[x,0]
                minIndex = x
            #print (arr[x,:])
    if (minScore != 100000):
        print ("\nBest score is: ")
        print (minScore)
        print (", path is: ")
        print (arr[minIndex, 2])
        return True, 0
    if (minScore == 100000):
        return False, rankIndex
    
def index_to_path(index):
    if index == 0:
        return "x"
    if index == 1:
        return "ax"
    if index == 2:
        return "y"
    if index == 3:
        return "ay"
    if index == 4:
        return "z"
    if index == 5:
        return "az"


if __name__ == "__main__":

    state = initial_state()
    print("Tutorial:\n This demo has two functions, \n#1 is manually scramble the rubiks cube,\n#2 is find all possible way to slove it in the max deep n,\n you need to manually scramble the rubik cube and give the maximun step\nhint: do not make it too complex, do not give a redicicously huge max step n, it will blow your memory\n(everything smaller than 5 is fine)")
    print("\n\nStep one: manually scramble the rubik cube, do not make it too complex")
    while True:
        
        print("Current state:")
        print(str(state))
        a = input("Enter an action ('x'=rotx, 'ax'=rot_ax, 'y'=roty, 'ay'=rot_ay, 'z'=rotz, 'az'=rot_az, 'q'=quit): ")
        if a == "x": state = state.rotx()
        if a == "ax": state = state.rot_ax()
        if a == "y": state = state.roty()
        if a == "ay": state = state.rot_ay() 
        if a == "z": state = state.rotz()
        if a == "az": state = state.rot_az()
        if a == "q": break
    
    print("\n\nStep two: input the max depth to solve: ")
    maxDepth = int(input())
    """
    print("\n\nStep three: input the max step  to solve: ")
    maxStep = int(input())
    """
    
    slove(state, maxDepth)
