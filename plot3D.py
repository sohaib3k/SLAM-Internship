import pandas as pd
import matplotlib as mpl
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import sys
import matplotlib.pyplot as plt
def plot3D(file1,file2):
	data_df = pd.read_csv(file1,delimiter = ' ',header=None)
	data_df2 = pd.read_csv(file2, delimiter = ' ',header=None)
	x = data_df[1]
	y = data_df[2]
	z = data_df[3]

	x1 = data_df2[1]
	y1 = data_df2[2]
	z1 = data_df2[3]

	xStart = x[:50]
	yStart = y[:50]
	zStart = z[:50]


	fig = plt.figure()
	ax = fig.gca(projection='3d')

	ax.plot(x1, y1, z1, label='pose graph_ORB')
	ax.plot(x, y, z, label='pose graph_GroundTruth_Start')
	ax.plot(xStart, yStart, zStart, label='pose graph_GroundTruth')
	ax.legend()

	plt.show()

plot3D(sys.argv[1],sys.argv[2])
