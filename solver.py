import networkx as nx
from parse import read_input_file, write_output_file
from utils import is_valid_solution, calculate_happiness
import sys
from os.path import basename, normpath
import glob

import math ##
from random import shuffle ##

def solve(G, s):
    """
    Args:
        G: networkx.Graph
        s: stress_budget
    Returns:
        D: Dictionary mapping for student to breakout room r e.g. {0:2, 1:0, 2:1, 3:2}
        k: Number of breakout rooms
    """
    # initialize variables
    n = len(list(G.nodes)) # num students
    k = max(2, math.ceil(n/(2*math.log2(n)))) # number of rooms
    rooms = {} # {room number: [list of students]} # {0: [1,2,3]}
    max_stress = s / k # max_stress = lambda: s / len(rooms)
    empty = {i for i in range(k)} # set of empty rooms
    unassigned = {i for i in range(n)} # set of unassigned students
    nonempty = {} # set of filled rooms
    
    # set all rooms as empty
    for i in range(k):
        rooms[i] = []
        
    # get largest happiness edge
    print(max([G[u][v]['happiness'] for (u, v) in G.edges()]))
    max_h = 0
    max_e = (0, 0)
    for (u, v) in G.edges():
        if (G[u][v]['happiness'] > max_h):
                max_h = G[u][v]['happiness']
                max_e = (u, v)
    print(max_h, max_e)
    
    # add u,v to same room
    rooms[0].extend(max_e[:])
    # remove from sets
    empty.remove(0)
    nonempty.add(0)
    unassigned.remove(max_e[0])
    unassigned.remove(max_e[1])
    print(rooms[0], unassigned)
    
    while len(unassigned) > 0:
        student = unassigned.pop()
        
        best_r = -1
        best_h = -1
        for room in nonempty:
            calculate_happiness_for_room(arr, G):
    
#    random_indices = random.sample(list(range(n)), n) # shuffles
#    room_size = int(n/k)
#    for i in range(k):
#        rooms[i] = random_indices[i]
    return {item:0 for item in range(n)}, k

# Here's an example of how to run your solver.

# Usage: python3 solver.py test.in

if __name__ == '__main__':
     assert len(sys.argv) == 2
     path = sys.argv[1]
     G, s = read_input_file(path)
     D, k = solve(G, s)
     assert is_valid_solution(D, G, s, k)
     print("Total Happiness: {}".format(calculate_happiness(D, G)))
     write_output_file(D, 'outputs/small-1.out')


# For testing a folder of inputs to create a folder of outputs, you can use glob (need to import it)
#if __name__ == '__main__':
#     inputs = glob.glob('inputs/*')
#     for input_path in inputs:
#         output_path = 'outputs/' + basename(normpath(input_path))[:-3] + '.out'
#         G, s = read_input_file(input_path)
#         D, k = solve(G, s)
#         assert is_valid_solution(D, G, s, k)
#         happiness = calculate_happiness(D, G)
#         write_output_file(D, output_path)
