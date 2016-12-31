# Wango The Robot
#
# this file takes continous pictures as long as face detection is not running.
# face detection and this process are exclusive.
import time
import cv2
import os.path
import sys
import os

try:
	import socket
	s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
	## Create an abstract socket, by prefixing it with null. 
	s.bind( '\0take_pictures_lock') 

except socket.error, e:
	error_code = e.args[0]
	error_string = e.args[1]
	print "Process already running (%d:%s ). Exiting" % ( error_code, error_string) 
	sys.exit (0)
	
else:
	turn_off_face_fname = "/var/www/html/turn_off_face.txt"
	done = False

	webcam = cv2.VideoCapture(-1)
	webcam.set(cv2.cv.CV_CAP_PROP_FRAME_WIDTH, 320)
	webcam.set(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT, 240)

	while not done:

		if not os.path.isfile(turn_off_face_fname):
			webcam.release()
			done=True
			exit()

		aframe = webcam.read()[1]
		cv2.imwrite("/mnt/ramdisk/image.jpg",aframe)
		time.sleep(0.1)
