import time, sys, os
from ros import rosbag
import roslib, rospy
roslib.load_manifest('sensor_msgs')
from sensor_msgs.msg import Image
import numpy as np
from cv_bridge import CvBridge
import cv2

TOPIC = 'camera/image_raw'

def CreateVideoBag(videopath, bagname):
    '''Creates a bag file with a video file'''
    bag = rosbag.Bag(bagname, 'w')
    try:
	text_file = open("rgb.txt", "w")
	text_file2 = open("timestamp.txt","w")
    except:
        print('Something went wrong! Can\'t tell what?')
    cap = cv2.VideoCapture(videopath)
    cb = CvBridge()
    prop_fps = cap.get(cv2.cv.CV_CAP_PROP_FPS)
    if prop_fps != prop_fps or prop_fps <= 1e-2:
        print "Warning: can't get FPS. Assuming 24."
        prop_fps = 24
    ret = True
    frame_id = 0
    newpath = r'rgb' 
    if not os.path.exists(newpath):
    	os.makedirs(newpath)
    os.chdir(os.getcwd() + "/rgb")
    #print os.getcwd()

    while(ret):
	try:
        	ret, frame = cap.read()
        	frame_id += 1
        	stamp = rospy.rostime.Time.from_sec(float(frame_id) / prop_fps)
	
		kernel = np.zeros((9,9),np.float32)
		kernel[4,4] = 2.0
		boxFilter = np.ones((9,9),np.float32)/81
		kernel = kernel - boxFilter
		custom = cv2.filter2D(frame,-1,kernel)
	
        	image = cb.cv2_to_imgmsg(custom, encoding='bgr8')
        	image.header.stamp = stamp
        	image.header.frame_id = "camera"
        	bag.write(TOPIC, image, stamp)
		cv2.imwrite("right" + str(frame_id) +".jpg",custom)
    		text_file.write(str(frame_id)+" " + "rgb/" + str(frame_id) +".jpg" + "\n")
    		text_file2.write(str(stamp) + " " + "0" + "\n")
	except:
		print "Missed a frame"
    cap.release()
    bag.close()

if __name__ == "__main__":
    if len( sys.argv ) == 3:
        CreateVideoBag(*sys.argv[1:])
    else:
        print( "Usage: video2bag videofilename bagfilename")
