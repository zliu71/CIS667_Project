# CIS667_Project
In milestone 2, I have two brand new files called 2x2x2new.py and 3x3x3new.py, those are the new projects I build for the milestone 2.
Each of these files have a step to step toturial that you can just run the file and following the build in instruction.
Here is the step to step instruction:
1. The only library I used is "numpy", you probably need to install the numply library in your environment before you run it.
2. To make sure everything is working properly, please using Python 3 to run the code(even it might be work in other versions, who knows).
3. Rules in "2x2x2new.py" and "3x3x3new.py" are identical, you can following the same toturial in both files.
Here is the toturial about how to run the code:
1. Scramble the rubik's cube manually.
2. Input an integer called "max depth", which is the accuracy of the heuristic.
3. Input an integer called "threshold", which is the accuracy of the A* algorithm.
4. Wait until you see the result pop out, it depends on how you scramble, max depth, threshold, and your CPU speed.
5. Input the "max_steps" which is the maximun step for random_process() to find the result.

~~In current state, there are two different games in this folder called 2x2x2rubiks.py and 3x3x3rubiks.py.
2x2x2rubkis.py is the workling platform I'm working on it, 3x3x3rubiks.py I still have multiple questions waiting to be answered.
In 2x2x2rubiks.py, there is only one library I have imported which is numpy, you need makesure there is a numpy library in your enviroment.
There is a specific step to play 2x2x2rubiks.py:
Step one, scramble the rubik's cube
there are 6 different command you can input, which is x, ax, y, ay, z, az, 
they are x axis 90 degree, x axis -90 degree, y axis 90 degree, y axis -90 degree, z axis 90 degree, and z axis -90 degree.
You can use these commands to scramble the Rubik's cube.
BUT you must be sure DO Not scramble too much, like scrumble more than 6 step; the more step you scramble the more time and memory you need to slove.
Step two, use iterative deepening search function to find the opssible way to slove, please do not input any number greater than 8, it will extremely slow,
1-6 still gonna be okey, but 7 will super slow, 8 is super super slow, 9 will blow your memory!~~
