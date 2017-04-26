import numpy as np
import networkx as nx

from bayesian_network import *

if __name__ == '__main__':
	nodes = ['praf','pmek','plcg','PIP2','PIP3','p44/42','pakts473','PKA','PKC','P38','pjnk']

	filePath = "data/1_quantile.csv"
	my_data = np.genfromtxt(filePath, delimiter=',', skip_header = 1)

	data = defaultdict(list)
	for idx, node in enumerate(nodes):
		data[node] = my_data.T[idx]

	bn = BayesianNetwork(node_list = nodes, edge_list = 'random', data = data)
	print bn.G.adj

	print bn.bic_score()
	# for node in bn.G.nodes():
	# 	ss = bn.get_ss(node, bn.G.predecessors(node))
		
	# 	print node
	# 	print ss
	#	print





