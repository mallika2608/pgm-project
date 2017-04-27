import numpy as np
import networkx as nx

from bayesian_network import *
from collections import defaultdict
from math import log

CONST_RANDOM_SEED = 42

np.random.seed(CONST_RANDOM_SEED)

# Computes sufficient statistics for a node
# Returns 2-d defaultdict indexed by index(value of node) and index(value of parents)
# where index(value of parents) = convertToBase10(value of parents considered as a base 3 string) 
def get_ss(data, node, parents = []):

	#Always consider parents in a fixed (sorted) order
	parents = sorted(parents)

	num_cols = 3 ** len(parents)
	
	ss = {}
	for i in xrange(3):
		ss[i] = defaultdict(int)

	for item_idx in xrange(len(data[node])):
		count_idx = 0
		base = 1
		for parent in parents:
			count_idx += data[parent][item_idx]*base
			base *= 3
		ss[data[node][item_idx]][count_idx] += 1

	return ss

# Marginalize parents over the child node
# e.g. P(X, Y, Z) -> P(X, Z), where Y is the child
def get_joint_counts(ss, parents_state):

	count = 0
	for i in ss:
		count += ss[i][parents_state]

	return count

#Needs data
def bic_local(data, node, parents):

	var_states = [0,1,2]
	state_counts = get_ss(data, node, parents)

	sample_size = len(data[node])
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
																log(var_state_count[state]) - log(get_joint_counts(state_counts, parents_state)) )  

	# Compute second term - H(Xi)
	term_2 = 0
	for state in var_states:
		term_2 += var_state_count[state] * ( log(sample_size) -  log(var_state_count[state]) )

	score = term_1 - term_2 

	# Subtract the penalty term
	score -= 0.5 * log(sample_size) * num_parents_state * (len(var_states) - 1)	

	return score

def bic_score(data, G):

	score = 0
	for node in G.nodes():
		score += bic_local(data, node, G.predecessors(node))

	return score
