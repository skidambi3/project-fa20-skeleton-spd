from parse import *
import re
import os
import random

import networkx as nx

import utils

G = nx.Graph()
for i in range(10):as
	G.add_node(i)
	for j in range(10):
		if i != j:
			G.add_node(j)
			G.add_edge(i, j)
stress_budget = 80.5
path = "./10.in"
write_input_file(G, stress_budget, path)