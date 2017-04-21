import sys
import os
from numpy import genfromtxt

fileDir = os.path.dirname(os.path.realpath(__file__))
dataDir = os.path.join(fileDir, "data")

fileName = "1. cd3cd28.csv"
filePath = os.path.join(dataDir, fileName)

def readDataFile():

	#with open(filePath, "r") as f:
	my_data = genfromtxt(filePath, delimiter=',')
	print my_data.shape

	my_data = my_data[1:] #removing header row
	#print my_data[:5]



if __name__ == '__main__':
	readDataFile()