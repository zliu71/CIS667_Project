import one_hot as oh
import generator as gr
import neuron_network as nn
import torch as tr
import numpy as np



def nn_choice(node):
    #stop tensor.backward
    with tr.no_grad():
        #input value
        x = tr.stack([tr.from_numpy(child.state.cube) for child in node.children()])
        y = net(x.reshape(len(x),2*2*2*3*6).float())
            
        #print(y)
        
        buf = 0
        ind = 0
        for i in range(len(y)):
            if buf < y[i]:
                buf = y[i]
                ind = i
            if buf == 8:
                return i
    #print(buf)
    #print(y[i])
    #print(node.children()[i].match)
    return ind

def manual_scramble():
    state = oh.initial_state()
    while True:
        print("Current state:")
        state.disp()
        a = input("Enter an action ('x'=rotx,'y'=roty, 'z'=rotz, 'q'=quit): ")
        if a == "x": state = state.rotx()
        if a == "y": state = state.roty()
        if a == "z": state = state.rotz()
        if a == "q": break
    return state

if __name__ == "__main__":
    game_mode = 0
    while game_mode != 4: 
        game_mode = int(input("\nPlease Choose the game to play:\n1. random solve rubik's cube\n2. A* solve rubik's cube\n3. A* NN solve rubik'cube\n4. Quit\nYou choose is: "))
        
        if (game_mode) == 1:
            print("\nScore is: %d" % oh.random_process_score(manual_scramble(), int(input("Please input the depth you want: "))))

        if (game_mode) == 2:
            oh.A_star_solve(manual_scramble(), int(input("Please input number of steps you want: ")), int(input("Please input the depth you want: ")))
        #input parameters
        if (game_mode) == 3:
            state = manual_scramble()
            scramble_depth = int(input("\nPlease input the module you want to load: "))
            depth = int(input("\nPlease input the number of depth: "))
            steps = int(input("\nPlease input the number of steps: "))

            node = gr.Node(state, depth, steps)
            
            #import trained nn
            net = nn.RubikNet()
            net.load_state_dict(tr.load("model_%d.pth" % scramble_depth))
            for step in range(steps):
                print("Turn %d" % step)
                #check goal
                if node.match == 8:
                    print("\nSolve")
                    print("Path is :")
                    print(node.path)
                    #node.state.disp()
                    break
                #check if have goal in the pool of children, in-other word, check the size of heuristic, it has the goal or not 
                #search if there is a result in the heuristic
                ind = gr.make_choice(node)
                #check goal in last step
                if node.children()[ind].match == 8:
                    print("\nHeuristic search Solve")
                    print("Path is :")
                    print(node.children()[ind].path)
                    node.children()[ind].state.disp()
                    break
                #no goal in the poll of children
                #nn_searching
        
                ind = nn_choice(node)
                print("\nNeuron network pick index: %d, score: %d" % (ind, node.children()[ind].score))
                node = node.children()[ind]
                #check goal before next turn
                if node.match == 8:
                    print("\nNeuron Solve")
                    print("Path is :")
                    print(node.path)
                    node.state.disp()
                    break
                print("\nCurrent match is: %d" % node.match)
                print("\nCurrent state is:")
                node.state.disp()
                input("\nPress Enter to continue")
            
