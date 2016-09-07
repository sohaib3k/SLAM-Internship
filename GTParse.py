import pandas as pd
import numpy as np
import sys
import argparse
##Pass Filename as Command line argument
def readCSV(filename,savename,secondTrajectory,secondTrajectorysavename):
	#Reading csv file
	data_df = pd.read_csv(filename,delimiter = ',',header=6,skiprows=[7])
	data_df2 = pd.read_csv(secondTrajectory,delimiter = ' ')

	print(data_df.columns)
	f = data_df['Frame']
	t = data_df['Time']
	xQ = data_df['X']
	yQ = data_df['Y']
	zQ = data_df['Z']
	w = data_df['W']
	x = data_df['X.1']
	y = data_df['Y.1']
	z = data_df['Z.1']
	
	##Conversion from mm to metres
	x = x/1000
	y = y/1000
	z = z/1000
	
	data_df['tx'] = x
	data_df['ty'] = y
	data_df['tz'] = z
	
	##Writing to new file
	dfNew = pd.concat([data_df['Time'], data_df['tx'],data_df['ty'],data_df['tz'],data_df['X'],data_df['Y'],data_df['Z'],data_df['W']], axis=1, 	keys=['timestamp' ,'tx' ,'ty' ,'tz' ,'qx', 'qy' ,'qz', 'qw'])

	dfNew.to_csv(savename, sep=' ',index=False, index_label=None,header=False)
	data_df2.to_csv(secondTrajectorysavename,sep=' ',index=False, index_label=None,header=False)


if __name__=="__main__":
	print "GroundTruth GroundTruthParsedfilename SecondTrajectory SecondTrajectoryParsedfilename"
	try:
		readCSV(sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4])
	except:
		print "Enter correct Format"





