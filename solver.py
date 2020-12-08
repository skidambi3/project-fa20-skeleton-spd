import networkx as nx
from parse import read_input_file, write_output_file
#from utils import is_valid_solution, calculate_happiness
from utils import *
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
#     # initialize variables
    
#     n = len(list(G.nodes)) # num students
#     k = max(2, math.ceil(n/(2*math.log2(n)))) # number of rooms
#     rooms = {} # {room number: [list of students]} # {0: [1,2,3]}
#     max_stress = s / k # max_stress = lambda: s / len(rooms)
#     empty = {i for i in range(k)} # set of empty rooms
#     unassigned = {i for i in range(n)} # set of unassigned students
#     nonempty = {} # set of filled rooms
    
#     # set all rooms as empty
#     for i in range(k):
#         rooms[i] = []
        
#     # get largest happiness edge
#     print(max([G[u][v]['happiness'] for (u, v) in G.edges()]))
#     max_h = 0
#     max_e = (0, 0)
#     for (u, v) in G.edges():
#         if (G[u][v]['happiness'] > max_h):
#                 max_h = G[u][v]['happiness']
#                 max_e = (u, v)
#     print(max_h, max_e)
    
#     # add u,v to same room
#     rooms[0].extend(max_e[:])
#     # remove from sets
#     empty.remove(0)
#     nonempty.add(0)
#     unassigned.remove(max_e[0])
#     unassigned.remove(max_e[1])
#     print(rooms[0], unassigned)
    
#     while len(unassigned) > 0:
#         student = unassigned.pop()
        
#         best_r = -1
#         best_h = -1
#         for room in nonempty:
#             calculate_happiness_for_room(arr, G):
    
# #    random_indices = random.sample(list(range(n)), n) # shuffles
# #    room_size = int(n/k)
# #    for i in range(k):
# #        rooms[i] = random_indices[i]
#     return {item:0 for item in range(n)}, k


    #check if u and v are in the same room
    def in_same_room(u, v):
        for room in rooms:
            if u in rooms[room] and v in rooms[room]:
                return False
        return True

    #returns what room u is in
    def room(u):
        for room in rooms:
            if u in rooms[room]:
                return room

    #check if we can put u in v's room
    def check(u, v):
        if in_same_room(u, v):
            return False
        room_u = room(u)
        room_v = room(v)

        #can we put u in v's room
        new_s = s/(len(rooms) - 1) if len(rooms[room_u]) == 1 else s/len(rooms)
        can_uv = calculate_stress_for_room(rooms[room_v] + u, G) < new_s

        return can_uv

        # #can we put v in u's room
        # new_s = s/(len(rooms) - 1) if len(room_v) == 1 else s/len(rooms)
        # can_vu = calculate_stress_for_room(room_u + v) > new_s: 
        
        # if can_uv or can_vu:
        #     return True
        # # return False

    #returns max valid edge
    def get_max_valid_edge():
        max_h = -1
        max_e = (-1, -1)
        for (u, v) in G.edges():
            print(check(u, v), check(v, u))
            if G[u][v]['happiness'] > max_h and in_same_room(u, v): #(check(u, v) or check(v, u)):
                print("in")
                max_h = G[u][v]['happiness']
                max_e = (u, v)
        return max_e

    from random import shuffle


    # #put u and v in the same room optimally (u in v's room or v in u's room)
    # def put(u, v):

    #     h_uv = -1
    #     h_vu = -1

    #     print(u, v)
    #     #calculate happiness if we put u in v's room
    #     if (check(u, v)):
    #         h_uv = calculate_happiness_for_room(rooms[room(v)] + [u], G)

    #     #calculate happiness if we put v in u's room
    #     else:
    #         h_vu = calculate_happiness_for_room(rooms[room(u)] + [v], G)

    #     #do the better one
    #     if h_uv > h_vu:
    #         #put u in v's room
    #         rooms[room_v].append(rooms[room_u].remove(u))
    #         if len(room(u)) == 0:
    #             rooms.pop(room(u))
    #     else:
    #         #put v in u's room
    #         rooms[room(u)].append(rooms[room(v)].remove(v))
    #         # if len(room(v)) == 0:
    #         #     rooms.pop(room(v))
    def get_happy_index(unassigned, lst, num_rooms):
        happy_ind = None
        happy_val = -1
        stress_val = 1

        happy_orig = calculate_happiness_for_room(lst, G)
        stress_orig = calculate_stress_for_room(lst, G)

        lst = [0] + lst

        for i in unassigned:
            lst[0] = i
            
            stress_cur = calculate_stress_for_room(lst, G) # < s / (num_rooms+1):
            if stress_cur < s / (num_rooms+1):
                happy_cur = calculate_happiness_for_room(lst, G)
                
                if happy_cur/(stress_cur+0.001) > happy_val/(stress_val+0.001):
                    happy_val = happy_cur
                    stress_val = stress_cur
                    happy_ind = i
            # if happy_val > happy_cur:
                # if calculate_stress_for_room(lst, G) < s / (num_rooms+1):
                #     happy_ind = i
                #     happy_val = happy_cur
        return happy_ind

    def get_stress_index(lst):
        stress_ind = 0
        stress_val = calculate_stress_for_room(lst[1:], G)
        lst.append(lst.pop(0))

        for i in range(1,len(lst)):
            val = lst.pop(0)
            
            stress_cur = calculate_stress_for_room(lst, G)
            if stress_cur < stress_val:
                stress_ind = i
                stress_val = stress_cur
            
            lst.append(val)
        return stress_ind


    n = len(list(G.nodes))
    rooms = {}
    # for i in range(n):
    #     rooms[i] = [i]
    max_stress = lambda: s / len(rooms)

    unassigned = {i for i in range(n)}
    num_rooms = 0
    while len(unassigned) > 0:
        rooms[num_rooms] = []
        
        while calculate_stress_for_room(rooms[num_rooms], G) < s / (num_rooms+1):
            max_ind = get_happy_index(unassigned, rooms[num_rooms], num_rooms)
            if max_ind == None:
                break
            rooms[num_rooms].append(max_ind)
            unassigned.remove(max_ind)

        # for i in unassigned:
            # If person can be added add them
            # find the highest happiness that still yields valid result
            
            # if i in unassigned and calculate_stress_for_room(rooms[num_rooms] + [i], G) < s / (num_rooms+1):
            #     rooms[num_rooms].append(i)
            #     unassigned.remove(i)
        for ind in range(num_rooms):
            # If any previous room exceeds stress budget, remove highest stress individuals
            while calculate_stress_for_room(rooms[ind], G) > s / (num_rooms+1):
                min_ind = get_stress_index(rooms[ind])
                unassigned.add(rooms[ind].pop(min_ind))
                # unassigned.add(rooms[ind].pop())
                ## fix this to be not random

            ## delete below

            while calculate_stress_for_room(rooms[ind], G) < s / (num_rooms+1):
                max_ind = get_happy_index(unassigned, rooms[ind], num_rooms)
                if max_ind == None:
                    break
                rooms[ind].append(max_ind)
                unassigned.remove(max_ind)

            ## delete above


        num_rooms += 1

    dic = convert_dictionary(rooms)
    #while not is_valid_solution
    rooms_dic = {}
    for num in range(len(rooms)):
        tmp = set()
        for person in rooms[num]:
            tmp.add(person)
        rooms_dic[num] = tmp

    condition = 0
    while False:
        #print('a')
        for i in range(len(rooms)):
            #print('b')
            if condition:
                break
            for j in range(i, len(rooms)):
                #print('c')
                if condition:
                    break

                breaker = False
                for a in rooms_dic[i]:
                    adic = rooms_dic[i]
                    a_happy = calculate_happiness_for_room(list(adic), G)
                    adic.remove(a)

                    for b in rooms_dic[j]:
                        bdic = rooms_dic[j]
                        b_happy = calculate_happiness_for_room(list(bdic), G)
                        bdic.remove(b)

                        adic.add(b)
                        bdic.add(a)
                        if calculate_stress_for_room(list(adic), G) < s / (num_rooms+1) and calculate_stress_for_room(list(bdic), G) < s / (num_rooms+1):
                            if a_happy + b_happy < calculate_happiness_for_room(list(adic), G) + calculate_happiness_for_room(list(bdic), G):
                                print('SWAP!!!!!')
                                condition += 1
                                breaker = True
                                break

                        adic.remove(b)
                        bdic.remove(a)

                        bdic.add(b)
                    if breaker:
                        break
                    adic.add(a)
            if breaker:
                break
        #break
        
    
        


    # while True:
    #     print("True")
    #     (u, v) = get_max_valid_edge()
    #     if (u, v) == (-1, -1):
    #         break
    #     put(u, v)
    # print(rooms)
    return (convert_dictionary(rooms), len(rooms))



# Here's an example of how to run your solver.

# Usage: python3 solver.py test.in

# if __name__ == '__main__':
#      assert len(sys.argv) == 2
#      path = sys.argv[1]
#      G, s = read_input_file(path)
#      D, k = solve(G, s)
#      assert is_valid_solution(D, G, s, k)
#      print("Total Happiness: {}".format(calculate_happiness(D, G)))
#      write_output_file(D, 'outputs/small-1.out')


# For testing a folder of inputs to create a folder of outputs, you can use glob (need to import it)
if __name__ == '__main__':
    inputs = glob.glob('inputs/*')
    for input_path in inputs:
        output_path = 'outputs/' + basename(normpath(input_path))[:-3] + '.out'
        G, s = read_input_file(input_path)
        D, k = solve(G, s)
        assert is_valid_solution(D, G, s, k)
        happiness = calculate_happiness(D, G)
        write_output_file(D, output_path)
