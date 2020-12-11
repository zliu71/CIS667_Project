import numpy as np
import torch as tr
from torch.nn import Sequential, Conv2d, Linear, Flatten, LeakyReLU, Tanh

def RubikNet():
    return tr.nn.Sequential(tr.nn.Flatten(), tr.nn.Linear((3*3*3*3*6),50), tr.nn.ReLU(), tr.nn.Linear(50,10), tr.nn.ReLU(), tr.nn.Linear(10,1), tr.nn.ReLU())

def calculate_loss(net, x, y_targ):
    size = x.size()
    batch_size = size[0]
    in_features = 1
    for i in size:
        if i != batch_size:
            in_features = in_features * i
    out_features = 1
    """
    e = 0
    for i in range(len(x[:,0])):
        weight_data = tr.randn(len(tr.flatten(x[i])),1)
        bias_data = tr.randn(len(tr.flatten(y_targ[i])),1)
        net.weight_data = weight_data
        net.bias_data = bias_data
        y = net(tr.flatten(x[i]))
        e = e + (y - y_targ[i])**2
    """
    net.weight_data = tr.randn(in_features,1)
    net.bias_data = tr.randn(out_features)
    y = net(x.reshape(batch_size, in_features))
    e = tr.sum((y - y_targ)**2)
    return (y, e)

def optimization_step(optimizer, net, x, y_targ):
    optimizer.zero_grad()
    y, e = calculate_loss(net, x, y_targ)
    e.backward()
    optimizer.step()
    return (y, e)

if __name__ == "__main__":

    scramble_depth = int(input("\nPlease input the scramble_depth: "))
    net = RubikNet()
    print(net)

    import pickle as pk
    with open("training_data_%d_scramble_depth.pkl" % scramble_depth, "rb") as f: (x, y_targ) = pk.load(f)

    # Optimization loop
    optimizer = tr.optim.Adam(net.parameters())
    train_loss, test_loss = [], []
    shuffle = np.random.permutation(range(len(x)))
    split = 10
    train, test = shuffle[:-split], shuffle[-split:]
    for epoch in range(200):
        y_train, e_train = optimization_step(optimizer, net, x[train], y_targ[train])
        y_test, e_test = calculate_loss(net, x[test], y_targ[test])
        if epoch % 10 == 0: print("%d: %f (%f)" % (epoch, e_train.item(), e_test.item()))
        train_loss.append(e_train.item() / (len(shuffle)-split))
        test_loss.append(e_test.item() / split)
    
    tr.save(net.state_dict(), "model_%d.pth" % scramble_depth)
    
    import matplotlib.pyplot as pt
    pt.plot(train_loss,'b-')
    pt.plot(test_loss,'r-')
    pt.legend(["Train","Test"])
    pt.xlabel("Iteration")
    pt.ylabel("Average Loss")
    pt.show()
    
    pt.plot(y_train.detach().numpy(), y_targ[train].detach().numpy(),'bo')
    pt.plot(y_test.detach().numpy(), y_targ[test].detach().numpy(),'ro')
    pt.legend(["Train","Test"])
    pt.xlabel("Actual output")
    pt.ylabel("Target output")
    pt.show()
