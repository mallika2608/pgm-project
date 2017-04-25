import numpy as np

import sys
import os

fileDir = os.path.dirname(os.path.realpath(__file__))
dataDir = os.path.join(fileDir, "data")
fileName = "2. cd3cd28icam2.csv"
filePath = os.path.join(dataDir, fileName)

def readDataFile():

	#with open(filePath, "r") as f:
	my_data = np.genfromtxt(filePath, delimiter=',')

	my_data = np.transpose( my_data[1:] ) #removing header row
	
	print my_data.shape

	return my_data

#Removes sets of observations in which the value of atleast one variable is an outlier
#Outliers defined as values lying further than 3*stddev from mean 
def remove_outliers(my_data):

	outlier_indices = set()

	for row in my_data:
		three_sigma = 3*np.std(row)
		avg = np.mean(row)
		for idx, item in enumerate(row):
			if( abs(item - avg) > three_sigma ):
				outlier_indices.add(idx)

	new_data = []
	for row in my_data:
		new_row = [ item for idx, item in enumerate(row) if idx not in outlier_indices ]
		new_data.append(new_row)

	new_data = np.array(new_data)
	print new_data.shape

	return new_data

def get_value(item, first_boundary, second_boundary):

	if(item <= first_boundary):
		return 0
	if(item <= second_boundary):
		return 1
	else:
		return 2

#Discretize the protein level values
#Modes supported - interval and quantile discretization
def discretize(my_data, mode = 'quantile'):

	new_data = []

	for row in my_data:

		if (mode == 'quantile'):
			first_boundary = np.percentile(row, 33.33)
			second_boundary = np.percentile(row, 66.66)

		elif (mode == 'interval'):
			row_min, row_max= np.min(row), np.max(row)
			interval_length = (row_max - row_min)/3.0

			first_boundary = row_min + interval_length
			second_boundary = row_min + 2*interval_length

		else:
			print 'Invalid mode for discretize function'
			sys.exit(1)

		new_row = [ get_value(item, first_boundary, second_boundary) for item in row ]
		#print new_row.count(0), new_row.count(1), new_row.count(2)
		new_data.append(new_row)

	new_data = np.array(new_data)
	#print new_data

	return new_data

if __name__ == '__main__':
	my_data = readDataFile()
	my_data = remove_outliers(my_data)
	#my_data = interval_discretize(my_data)
	my_data = discretize(my_data, 'quantile')
	np.savetxt("data/2_quantile_discretized.csv", my_data.T, delimiter = ",", fmt = '%d')