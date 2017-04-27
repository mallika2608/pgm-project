import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

from bayesian_network import *
from scoring import *
from copy import deepcopy
from collections import defaultdict
from math import log, exp

CONST_RANDOM_SEED = 42

np.random.seed(CONST_RANDOM_SEED)

def add_edge(G, u, v):

	copyG = G.copy()
	copyG.add_edge(u, v)
	if( not nx.is_directed_acyclic_graph(copyG) ):
		#print "Loop detected. Edge {0}->{1} could not be added.".format( u, v )
		raise ValueError("Loop detected")
	else:
		G.add_edge(u, v)

def remove_edge(G, u, v):

	G.remove_edge(u, v)

def reverse_edge(G, u, v):

	copyG = G.copy()
	copyG.remove_edge(u, v)
	copyG.add_edge(v, u)

	if( not nx.is_directed_acyclic_graph(copyG) ):
		#print "Loop detected. Edge {0}->{1} could not be reversed.".format( u, v )
		raise ValueError("Loop detected")
	else:
		G.remove_edge(u, v)
		G.add_edge(v, u)


def stochastic_hill_climbing_search(data, network, max_iters = 500):

	steps = 0
	G_best = deepcopy(network.G)

	while steps < max_iters:

		G_o = deepcopy(G_best)

		#Choose type of next move
		move_type = np.random.randint(3)

		#If there are no edges, we can only add an edge
		if(len(G_o.edges()) == 0): move_type = 0

		if(move_type == 0):
			#Add edge
			u = np.random.choice(G_o.nodes())
			v = np.random.choice(G_o.nodes())

			while G_o.has_edge(u,v) or u==v:
				u = np.random.choice(G_o.nodes())
				v = np.random.choice(G_o.nodes())
			
			try:
				add_edge(G_o, u, v)
			except ValueError as err:
				continue

		elif(move_type == 1):
			#Delete edge
			rand_idx = np.random.randint(len(G_o.edges())) 
			u, v = G_o.edges()[rand_idx]
			
			try:
				remove_edge(G_o, u, v)
			except ValueError as err:
				continue

		else:
			#Reverse edge
			rand_idx = np.random.randint(len(G_o.edges()))
			u, v = G_o.edges()[rand_idx]
			
			try:
				reverse_edge(G_o, u, v)
			except ValueError as err:
				continue

		if(bic_score(data, G_o) > bic_score(data, G_best)):
			G_best = deepcopy(G_o)

		steps += 1

	print bic_score(data, G_best)

	network.G = G_best

	return network

def greedy_hill_climbing_search(data, network):

	success = 0
	G_best = deepcopy(network.G)

	converged = False

	while not converged:
	
	 	G_current = deepcopy(G_best)

	 	# Try all deletions
		for edge in G_current.edges():

			G_o = deepcopy(G_current)
			u, v = edge
			
			try:
				remove_edge(G_o, u, v)
			except ValueError as err:
				continue

			if(bic_score(data, G_o) > bic_score(data, G_best)):
				G_best = deepcopy(G_o)

		# Try all reversions
		for edge in G_current.edges():

			G_o = deepcopy(G_current)
			u, v = edge

			try:
				reverse_edge(G_o, u, v)
			except ValueError as err:
				continue

			if(bic_score(data, G_o) > bic_score(data, G_best)):
				G_best = deepcopy(G_o)

		# Try all additions
		for u in G_current.nodes():
			for v in G_current.nodes():
				if ( u != v and not G_current.has_edge(u,v) ) :
					
					G_o = deepcopy(G_current)

					try:
						add_edge(G_o, u, v)
					except ValueError as err:
						continue

					if(bic_score(data, G_o) > bic_score(data, G_best)):
						G_best = deepcopy(G_o)

		if( abs(bic_score(data, G_best) - bic_score(data, G_current))  < 1e-3 ): 
			converged = True

	print bic_score(data, G_best)

	network.G = G_best

	return network

def acceptance_probability(old_cost, new_cost, temp):

	return exp( min(1, (old_cost - new_cost) / float(temp) ) )

def simulated_annealing(data, network):

	temp = 1.0
	temp_min = 0.35
	alpha = 0.8

	G_best = deepcopy(network.G)

	while temp > temp_min:
	
	 	i = 1

	 	print "Current temp ", temp

	 	while i <= 10:

			G_o = deepcopy(G_best)

			#Choose type of next move
			move_type = np.random.randint(3)

			#If there are no edges, we can only add an edge
			if(len(G_o.edges()) == 0): move_type = 0

			if(move_type == 0):
				#Add edge
				u = np.random.choice(G_o.nodes())
				v = np.random.choice(G_o.nodes())

				while G_o.has_edge(u,v) or u==v:
					u = np.random.choice(G_o.nodes())
					v = np.random.choice(G_o.nodes())
				
				try:
					add_edge(G_o, u, v)
				except ValueError as err:
					continue

			elif(move_type == 1):
				#Delete edge
				rand_idx = np.random.randint(len(G_o.edges())) 
				u, v = G_o.edges()[rand_idx]
				
				try:
					remove_edge(G_o, u, v)
				except ValueError as err:
					continue

			else:
				#Reverse edge
				rand_idx = np.random.randint(len(G_o.edges()))
				u, v = G_o.edges()[rand_idx]
				
				try:
					reverse_edge(G_o, u, v)
				except ValueError as err:
					continue

			new_cost = bic_score(data, G_o)
			old_cost = bic_score(data, G_best)

			ap = acceptance_probability(old_cost, new_cost, temp)
			print "Temp, ap : ", temp, ap
			if ap > np.random.random():
				G_best = deepcopy(G_o)

			i += 1
		
		temp = temp * alpha

	print bic_score(data, G_best)

	network.G = G_best

	return network