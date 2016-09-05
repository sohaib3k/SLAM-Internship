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
	right =  sorted(glob.glob('right/*.png'),key=numericalSort)
	left =  sorted(glob.glob('left/*.png'),key=numericalSort)
    	try:
		text_file = open("rgb.txt", "w")
		text_file2 = open("timestamp.txt","w")
    	except:
        	print('Something went wrong! Can\'t tell what?')
	print "Total Images " + str(len(right))
    	bag = rosbag.Bag("stereoBag", 'w')
	cb = CvBridge()
	frame_id = 0
	dummyImage = cv2.imread('dummy.jpg')
	dummyMessage = cb.cv2_to_imgmsg(dummyImage, encoding='bgr8')
	for x in range(len(right)):
		
        	stamp = rospy.rostime.Time.from_sec(float(frame_id) / 59)
		leftImg = cv2.imread(left[x])
		print "left = " + str(left[x])
		frame_id +=1
		rightImg = cv2.imread(right[x])
		print "right = " + str(right[x])

		kernel = np.zeros((9,9),np.float32)
		kernel[4,4] = 4.0
		boxFilter = np.ones((9,9),np.float32)/81
		kernel = kernel - boxFilter
		customL = cv2.filter2D(leftImg,-1,kernel)
		customR = cv2.filter2D(rightImg,-1,kernel)

        	image = cb.cv2_to_imgmsg(customL, encoding='bgr8')
        	image2 = cb.cv2_to_imgmsg(customR, encoding='bgr8')
        	image.header.stamp = stamp
        	image.header.frame_id = "camera"
        	image2.header.stamp = stamp
        	image2.header.frame_id = "camera"
		#if frame_id <353:
        		#bag.write("cam0/image_raw", dummyMessage, stamp)
        		#bag.write("cam1/image_raw", dummyMessage, stamp)
		#else:
    		text_file.write(str(frame_id)+" " + "rgb/" + str(frame_id) +".png" + "\n")
    		text_file2.write(str(stamp) + " " + "0" + "\n")
       		bag.write("cam0/image_raw", image, stamp)
       		bag.write("cam1/image_raw", image2, stamp)
	bag.close()
CreateVideoBag()



