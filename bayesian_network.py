import networkx as nx
import numpy as np

CONST_RANDOM_SEED = 42

np.random.seed(CONST_RANDOM_SEED)

class BayesianNetwork():

	def __init__(self, node_list = None, edge_list = None):

		self.G = nx.DiGraph()

		if(edge_list == 'random'):

			np.random.shuffle(node_list)
			self.G.add_nodes_from(node_list)

			baseRandomG = nx.gnp_random_graph(len(node_list),0.33,directed=True, seed=CONST_RANDOM_SEED)
			self.G = nx.DiGraph([(node_list[u], node_list[v]) for (u,v) in baseRandomG.edges() if u < v ])
		
		else:

			self.G.add_nodes_from(node_list)

			for (u,v) in edge_list:
				self.add_edge(u,v)

	def add_edge(self, u, v):

		copyG = self.G.copy()
		copyG.add_edge(u, v)
		if( not nx.is_directed_acyclic_graph(copyG) ):
			#Cycle detected
			print "Loop detected. Edge {0}->{1} could not be added.".format( u, v )
			pass
		else:
			self.G.add_edge(u, v)