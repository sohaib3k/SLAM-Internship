import time, sys, os
from ros import rosbag
import roslib, rospy
roslib.load_manifest('sensor_msgs')
from sensor_msgs.msg import Image
import numpy as np
from cv_bridge import CvBridge
import cv2
import re
import glob

TOPIC = 'camera/image_raw'
numbers = re.compile(r'(\d+)')
def numericalSort(value):
    parts = numbers.split(value)
    parts[1::2] = map(int, parts[1::2])
    return parts
def CreateVideoBag(LOC):
	right =  sorted(glob.glob(LOC),key=numericalSort)
	print "Total Images " + str(len(right))
    	bag = rosbag.Bag("monoBag", 'w')
	cb = CvBridge()
	frame_id = 161
	time = 11.666667;
	frame = 0.066666667;
	for x in range(len(right)):
		
        	stamp = rospy.rostime.Time.from_sec(time + frame)
		
		frame_id +=1
		rightImg = cv2.imread(right[x])


		kernel = np.zeros((9,9),np.float32)
		kernel[4,4] = 3.0
		boxFilter = np.ones((9,9),np.float32)/81
		kernel = kernel - boxFilter

		customR = cv2.filter2D(rightImg,-1,kernel)


        	image2 = cb.cv2_to_imgmsg(rightImg, encoding='bgr8')

        	image2.header.stamp = stamp
        	image2.header.frame_id = "camera"
		
       		bag.write("camera/image_raw", image2, stamp)

	bag.close()
	if __name__ == "__main__":
    if len( sys.argv ) == 2:
        CreateVideoBag(*sys.argv[2])
    else:
        print( "Usage: Record_02/*.png")




