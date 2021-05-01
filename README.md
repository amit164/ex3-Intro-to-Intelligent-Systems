# ex3-Intro-to-Intelligent-Systems
This is an executive implementation that acts using behavior selection approach

1. [Introduction](#introduction)  
2. [Dependencies](#dependencies)
3. [Installation](#installation)

## Introduction
This is an agent that decide in each step what is the best behavior and act accordingly. The agent solves two domains - maze and football - it won't work on any other domain because it relieis those predicates and actions. 
These two domains are Not deterministic, the effects of each action can be different according to a given probability function.

The agent holds a graph that represents the world. In general, the ``` next_action()``` diveds the agent to two parts - maze and football in order to choose the best behavior. In poth parts, I consider the probability to sucsess in a move and I chose to calculate the distance by "The higher the probability, the less distance".

##### Maze:
The agent go throgh all options to action and pick goal that relevant to the player that can make this option.
If this player is relevant (there is a goal that includes it), the agent checks the distance between the point it wiil be if it will do this action to goal and finds the minimum distance from all options (and players).
> Note: if there is more than one goal that relevant to this player, the agent will chose it randomly.

##### Football:
The agent finds all relevant balls to the goal. For every ball, the agent checks the distance between the robot and the ball. If the robot and the ball is in the same place, the agent chooses the best **kick** action. Otherwise, the agent finds the minimum distance from it place to **goal** by calculating the formula: 

<div align="center"> <em> 0.5 * distance to ball^2 + 0.2 * distance between ball and the goal^3 </em> </div><br/>

I chose this formula because the probability to sucsess a kick action is higher than the probability to move do a direction. 
Then, the agent looks after an option that includes the first place of the shortest pathand choose it.

In order to implement this agent, I created a Grapgh data structure using [this](https://www.geeksforgeeks.org/generate-graph-using-dictionary-python/) implementation.  
Also, in order to find the shortest path I used a BFS algorithem I found [here](https://www.geeksforgeeks.org/shortest-path-unweighted-graph/)

## Dependencies:
* Ubuntu16 O.S
* python 2.7.18
* pddlsim (more info [here](https://bitbucket.org/galk-opensource/executionsimulation/src/master/))

## Installation:
1. Clone the repository:  
    ```
    $ git clone https://github.com/amit164/ex3-Intro-to-Intelligent-Systems.git
    ```
2. Write those commands in the terminal:
    ```
    $ cd ex3-Intro-to-Intelligent-Systems
    $ python my_executive <domain_file> <problem_file>
    ```
    > _domain_file_ is one of the domains uploaded here (maze_domain_multi_effect.pddl or simple_football_domain_multi.pddl)
 
    > _problem_file_ is a problem file for the domain you chose. You can use one of those here or create one of your own.
