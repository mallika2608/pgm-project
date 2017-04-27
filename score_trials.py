import numpy as np
import networkx as nx

from bayesian_network import *
from search import *

if __name__ == '__main__':
	nodes = ['A', 'B']

	filePath = "data/trial.csv"
	my_data = np.genfromtxt(filePath, delimiter=',', skip_header = 1)

	data = defaultdict(list)
	for idx, node in enumerate(nodes):
		data[node] = my_data.T[idx]

	bn = BayesianNetwork(node_list = nodes, edge_list = [('A','B')], data = data)

	print bic_score(data, bn.G)
