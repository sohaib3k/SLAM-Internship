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
def CreateVideoBag():
	right =  sorted(glob.glob('pics_30-1-17/*.png'),key=numericalSort)
	print "Total Images " + str(len(right))
    	bag = rosbag.Bag("monoBag", 'w')
	cb = CvBridge()
	frame_id = 565
	time = 18.333333333;
	frame = 0.033333333;
	for x in range(len(right)):
		time = time+frame
		print time
        	stamp = rospy.rostime.Time.from_sec(time)
		
		frame_id +=1
		rightImg = cv2.imread(right[x])


		kernel = np.zeros((9,9),np.float32)
		kernel[4,4] = 4.0
		boxFilter = np.ones((9,9),np.float32)/81
		kernel = kernel - boxFilter

		customR = cv2.filter2D(rightImg,-1,kernel)


        	image2 = cb.cv2_to_imgmsg(rightImg, encoding='bgr8')

        	image2.header.stamp = stamp
        	image2.header.frame_id = "camera"
		#if frame_id > 175:
			#print frame_id
			#time = time+frame;
       		bag.write("camera/image_raw", image2, stamp)

		#else:
		#	print "Missed"



	bag.close()
	print frame_id
CreateVideoBag()



