import networkx as nx
import numpy as np

from collections import defaultdict
from math import log

CONST_RANDOM_SEED = 42

np.random.seed(CONST_RANDOM_SEED)

class BayesianNetwork():

	def __init__(self, node_list = [], edge_list = [], data = None):

		self.G = nx.DiGraph()
		
		if(edge_list == 'random'):

			#np.random.shuffle(node_list) #Should this be used? Might help in randomizing the initial direction of the edges. Unsure.
			
			self.G.add_nodes_from(node_list)

			baseRandomG = nx.gnp_random_graph(len(node_list), 0.2, directed=True, seed=CONST_RANDOM_SEED)
			self.G.add_edges_from( [(node_list[u], node_list[v]) for (u,v) in baseRandomG.edges() if u < v ] )
			assert(nx.is_directed_acyclic_graph(self.G))
		
		else:

			self.G.add_nodes_from(node_list)

			for (u,v) in edge_list:
				self.add_edge(u,v)

		if(data == None):
			self.data = defaultdict(list)
		else:
			self.data = data

	def add_edge(self, u, v):

		copyG = self.G.copy()
		copyG.add_edge(u, v)
		if( not nx.is_directed_acyclic_graph(copyG) ):
			#Cycle detected
			print "Loop detected. Edge {0}->{1} could not be added.".format( u, v )
			pass
		else:
			self.G.add_edge(u, v)


	# Computes sufficient statistics for a node
	# Returns 2-d defaultdict indexed by index(value of node) and index(value of parents)
	# where index(value of parents) = convertToBase10(value of parents considered as a base 3 string) 
	def get_ss(self, node, parents = []):

		#Always consider parents in a fixed (sorted) order
		parents = sorted(parents)

		num_cols = 3 ** len(parents)
		
		ss = {}
		for i in xrange(3):
			ss[i] = defaultdict(int)

		for item_idx in xrange(len(self.data[node])):
			count_idx = 0
			base = 1
			for parent in parents:
				count_idx += self.data[parent][item_idx]*base
				base *= 3
			ss[self.data[node][item_idx]][count_idx] += 1

		return ss

	# Marginalize parents over the child node
	# e.g. P(X, Y, Z) -> P(X, Z), where Y is the child
	def get_joint_counts(self, ss, parents_state):

		count = 0
		for i in ss:
			count += ss[i][parents_state]

		return count

	def bic_local(self, node, parents):

		var_states = [0,1,2]
		state_counts = self.get_ss(node, parents)

		sample_size = len(self.data[node])
		num_parents_state = 3**len(parents)

		score = 0

		var_state_count = {}
		for i in state_counts:
			total = 0
			for k in state_counts[i]:
				total += state_counts[i][k]
			var_state_count[i] = total

		# Compute first term - I(Xi;Pai)
		term_1 = 0
		for parents_state in range(num_parents_state):
			for state in var_states:
				if state_counts[state][parents_state] > 0:
					term_1 += state_counts[state][parents_state] * ( log(state_counts[state][parents_state]) + log(sample_size) - 
																	log(var_state_count[state]) - log(self.get_joint_counts(state_counts, parents_state)) )  

		# Compute second term - H(Xi)
		term_2 = 0
		for state in var_states:
			term_2 += var_state_count[state] * ( log(sample_size) -  log(var_state_count[state]) )

		score = term_1 - term_2 

		# Subtract the penalty term
		score -= 0.5 * log(sample_size) * num_parents_state * (len(var_states) - 1)	

		return score

	def bic_score(self):

		score = 0
		for node in self.G.nodes():
			score += self.bic_local(node, self.G.predecessors(node))

		return score