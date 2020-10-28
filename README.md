# CIS667_Project
In current state, there are two different games in this folder called 2x2x2rubiks.py and 3x3x3rubiks.py.
2x2x2rubkis.py is the workling platform I'm working on it, 3x3x3rubiks.py I still have multiple questions waiting to be answered.
In 2x2x2rubiks.py, there is only one library I have imported which is numpy, you need makesure there is a numpy library in your enviroment.
There is a specific step to play 2x2x2rubiks.py:
Step one, scramble the rubik's cube
there are 6 different command you can input, which is x, ax, y, ay, z, az, 
they are x axis 90 degree, x axis -90 degree, y axis 90 degree, y axis -90 degree, z axis 90 degree, and z axis -90 degree.
You can use these commands to scramble the Rubik's cube.
BUT you must be sure DO Not scramble too much, like scrumble more than 6 step; the more step you scramble the more time and memory you need to slove.
Step two, use iterative deepening search function to find the opssible way to slove, please do not input any number greater than 8, it will extremely slow,
1-6 still gonna be okey, but 7 will super slow, 8 is super super slow, 9 will blow your memory!
