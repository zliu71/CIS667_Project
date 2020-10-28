import numpy as np

class RubiksState(object):
    def __init__(self):
        self.cube = np.zeros((6,3,3),dtype = int)
        
def initial_state():
    state = RubiksState()
    state.cube[:,:,:] = 0
    return state

if __name__=="__main__":
    state = initial_state()
    print("This function still working in progress, basically is a test platform for n x n x 6 array\nRight now I have no idea how to implement this function in single 1 to implement the color\nIf you want to scramble the rubiks cube please use another file 2x2x2rubiks.py")
    print (state.cube)
    
