import one_hot as oh
import generator as gr
import neuron_network as nn
import torch as tr
import numpy as np

#input parameters
num_games = int(input("\nPlease input the number of games: "))
scramble_depth = int(input("\nPlease input the number of scramble_depth: "))
depth = int(input("\nPlease input the number of depth: "))
steps = int(input("\nPlease input the number of steps: "))

#import trained nn
net = nn.RubikNet()
net.load_state_dict(tr.load("model_%d.pth" % scramble_depth))

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

if __name__ == "__main__":
    r_rand = list()
    r_A = list()
    r_A_nn = list()
    
    for game in range(num_games):
        scramble = gr.scramble(scramble_depth)
        
        
        #random choice
        print("\nCalculate random process game: %d" % game)
        r_rand.append(oh.random_process_score(scramble, (depth*steps)))
        #r_rand.append(oh.random_process_score(gr.scramble(scramble_depth), (depth*steps)))
        #A* choice
        print("\nCalculate A* game: %d" % game)
        r_A.append(oh.A_star_solve_score(scramble, steps, depth))
        #r_A.append(oh.A_star_solve_score(gr.scramble(scramble_depth), steps, depth))
        #A*_NN choice
        print("\nCalculate A*_NN game: %d" % game)
        node = gr.Node(scramble, depth, steps)
        #node = gr.Node(gr.scramble(scramble_depth), depth, steps)
        for step in range(steps):
            #check goal
            if node.match == 8:
                break
        
            #check if have goal in the pool of children, in-other word, check the size of heuristic, it has the goal or not 
            #search if there is a result in the heuristic
            ind = gr.make_choice(node)
            #check goal in last step
            if node.children()[ind].match == 8:
                node = node.children()[ind]
                break
            #no goal in the poll of children
            #nn_searching
            ind = nn_choice(node)
            node = node.children()[ind]
            
        r_A_nn.append(node.score)

    print(r_rand)
    print(r_A)
    print(r_A_nn)
    x = np.zeros((num_games, 3), int)
    x[:,0] = np.array(r_rand)
    x[:,1] = np.array(r_A)
    x[:,2] = np.array(r_A_nn)
    import matplotlib.pyplot as pt
    #pt.hist(r_rand,[3])
    #pt.hist(r_A,[3])
    #pt.hist(r_A_nn,[3])
    pt.hist(x)
    pt.legend(["random","A*","A*_NN"])
    pt.xlabel("Score")
    pt.ylabel("Games")
    pt.show()
    r_comp = np.array(r_A) - np.array(r_A_nn)
    pt.plot(r_comp, 'r-')
    pt.legend(["A* - A*nn"])
    pt.xlabel("Games")
    pt.ylabel("Score")
    pt.show()
    
        
