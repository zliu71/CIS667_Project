import itertools as it
import numpy as np
import torch as tr
import neuron_network as nn
import one_hot as oh
import generator as gr
#input the scramble_depth
scramble_depth = int(input("\nPlease input the scramble_depth: "))

depth = int(input("\nPlease input the depth: "))

steps = int(input("\nPlease input the steps: "))

#import the trained nn
net = nn.RubikNet()
net.load_state_dict(tr.load("model_%d.pth" % scramble_depth))


def nn_choice(node):
    #stop tensor.backward
    with tr.no_grad():
        #input value
        x = tr.stack([tr.from_numpy(child.state.cube) for child in node.children()])
        y = net(x.reshape(len(x),2*2*2*3*6).float())
            
        print(y)
        
        buf = 0
        for i in range(len(y)):
            if buf < y[i]:
                buf = y[i]
            if buf == 8:
                return i
    print(buf)
    return i
        
#the whole process in this main function is an A* searching algorithm using nn_network prune the unnecessary branch
if __name__ == "__main__":
    state = gr.scramble(scramble_depth)
    print("The scrambled Rubik's cube is:")
    state.disp()
    node = gr.Node(state, depth, steps)
    for step in range(steps):
        print("Turn %d" % step)
        #check goal
        if node.match == 8:
                print("\nSolve")
                print("Path is :")
                print(node.path)
                #node.state.disp()
                break
        #check if have goal in the poll of children, in-other word, check the size of heuristic, it has the goal or not 
        #search if there is a result in the heuristic
        ind = gr.make_choice(node)
        #check goal in last step
        if node.children()[ind].match == 8:
                print("\nSolve")
                print("Path is :")
                print(node.children()[ind].path)
                node.children()[ind].state.disp()
                break
        #no goal in the poll of children
        #nn_searching
        ind = nn_choice(node)
        print("\nNeuron network pick index %d" % ind)
        node = node.children()[ind]
        #check goal before next turn
        if node.match == 8:
                print("\nSolve")
                print("Path is :")
                print(node.path)
                node.state.disp()
                break
        print("\nCurrent match is: %d" % node.match)
        print("\nCurrent state is:")
        node.state.disp()
        

    
