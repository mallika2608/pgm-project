import numpy as np
import networkx as nx

import timeit

from bayesian_network import *
from search import *
from scoring import *

if __name__ == '__main__':
	nodes = ['praf','pmek','plcg','PIP2','PIP3','p44/42','pakts473','PKA','PKC','P38','pjnk']

	filePath = "data/2_interval_full.csv"
	my_data = np.genfromtxt(filePath, delimiter=',', skip_header = 1)

	optimal_edges = [('PKC', 'pjnk'), ('PKC', 'P38'), ('PKC', 'PKA'), ('PKC', 'praf'), ('PKC', 'pmek'),
('PKA', 'pjnk'), ('PKA', 'P38'), ('PKA', 'pakts473'), ('PKA', 'p44/42'), ('PKA', 'pmek'), ('PKA', 'praf'),
('praf', 'pmek'), ('pmek', 'p44/42'), ('p44/42', 'pakts473'),
('plcg','PIP2'), ('plcg','PIP3'), ('PIP3', 'PIP2')]

	data = defaultdict(list)
	for idx, node in enumerate(nodes):
		data[node] = my_data.T[idx]

	bn = BayesianNetwork(node_list = nodes, edge_list = optimal_edges, data = data)

	print "Optimal graph BIC score"
	print bic_score(data, bn.G)

	start_time = timeit.default_timer()
	best_bn = stochastic_hill_climbing_search(data, bn, max_iters = 500)
	elapsed = timeit.default_timer() - start_time

	print "Stochastic hill climbing time : ", elapsed

	nx.draw_networkx(best_bn.G, pos = nx.circular_layout(best_bn.G))
	plt.savefig("plots/shc_optimal.png")
	plt.clf()

	# bn = BayesianNetwork(node_list = nodes, edge_list = 'random', data = data)
	
	# start_time = timeit.default_timer()
	# best_bn = simulated_annealing(data, bn)
	# elapsed = timeit.default_timer() - start_time

	# print "Simulated annealing climbing time : ", elapsed

	# nx.draw_networkx(best_bn.G, pos = nx.circular_layout(best_bn.G))
	# plt.savefig("plots/simal_2_full_random.png")
	# plt.clf()

	# bn = BayesianNetwork(node_list = nodes, edge_list = 'random', data = data)

	# start_time = timeit.default_timer()
	# best_bn = greedy_hill_climbing_search(data, bn)
	# elapsed = timeit.default_timer() - start_time

	# print "Greedy hill climbing time : ", elapsed

	# nx.draw_networkx(best_bn.G, pos = nx.circular_layout(best_bn.G))
	# plt.savefig("plots/ghc_2_full_random.png")
	# plt.clf()
