# CIS667_Project
Everything you need to run is in the Final Report folder.
There are two projects, one is 2x2x2 Rubik's cube and another is Rubik's 3x3x3 cube.
In 2x2x2 folder:
1. Please make sure you have python 3.0 or higher in your environment
2. please make sure you have pytorch installed, otherwise pip install torch
3. please make sure you have numpy installed, otherwise pip install numpy

If you want to play the game, run play.py and just follow the instruction, you can set any steps as much as you want, but do not set depth more than 6, it will super slow.
If you want to generate the trainning data to train a new module, use generator.py generate data.
If you want to training a module, use neuron_network.py, the default epoch is 200.
If you want to check the lab report result, use compare_results.py.
If you don't want see anthing from previous milestone, use nn_rubik.py, that is the new algorithm based on A* and NN.
3x3x3 just same as 2x2x2, the only difference is the running speed is much slower than 2x2x2.
