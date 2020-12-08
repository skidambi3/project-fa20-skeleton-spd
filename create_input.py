from parse import *
import re
import os
import random
import math

import networkx as nx

import utils

#constants
n = 50
G = nx.Graph()
k = max(2, math.ceil(n/(2*math.log2(n))))
num_rooms = math.ceil(n/k)

def random_decimal(a, b):
    a, b = int(a), int(b)
    return round(((b - a) * random.random() + a)/n, 3)

#initialize graph
for i in range(n):
	G.add_node(i)
	for j in range(n):
		if i != j:
			G.add_node(j)
			G.add_edge(i, j, happiness = -1, stress = -1)

#initialize edges
max_room_stress = 0
nodes = list(G.nodes)
rooms = {}
r = 0
while len(nodes):
	room_stress = 0
	random.shuffle(nodes)
	room = nodes[0:k]
	nodes = nodes[k:]
	for i in room:
		rooms[i] = r
	r += 1
	#initialize edges in room
	for i in room:
		for j in room:
			if i < j:
				rand_h = random_decimal(20, 40)
				rand_s = random_decimal(5, 25)
				G[i][j]['happiness'] = rand_h
				G[i][j]['stress'] = rand_s
				room_stress += G[i][j]['stress']

	#initialize edges out of room
	for i in room:
		for j in nodes:
			rand_h = random_decimal(5, 25)
			rand_s = random_decimal(20, 40)
			G[i][j]['happiness'] = rand_h
			G[i][j]['stress'] = rand_s

	#update max stress per room
	max_room_stress = max(room_stress, max_room_stress)

#set the stress budget
stress_budget = math.ceil(max_room_stress*num_rooms + 0.1)
path_in = "./{}.in".format(n)
path_out = "./{}.out".format(n)
write_input_file(G, stress_budget, path_in)
write_output_file(rooms, path_out)
print("Input file validation: " + str(read_input_file(path_in)))
print("Output file validation: " + str(read_output_file(path_out, G, stress_budget)))

