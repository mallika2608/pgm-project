import numpy as np
import networkx as nx

from bayesian_network import *

if __name__ == '__main__':
	nodes = ['praf','pmek','plcg','PIP2','PIP3','p44/42','pakts473','PKA','PKC','P38','pjnk']

	bn = BayesianNetwork(node_list = nodes, edge_list = [('praf','pmek'), ('pmek', 'P38'), ('P38', 'praf') ])
	print nx.is_directed_acyclic_graph(bn.G)
	print bn.G.adj




