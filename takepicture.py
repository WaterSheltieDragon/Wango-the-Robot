import time
import cv2
import os.path
import sys
import os

turn_off_face_fname = "/var/www/html/turn_off_face.txt"
done = False

if __name__ == '__main__':

	webcam = cv2.VideoCapture(-1)                           # Get ready to start getting images from the webcam
	webcam.set(cv2.cv.CV_CAP_PROP_FRAME_WIDTH, 320)         # I have found this to be about the highest-
	webcam.set(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT, 240)        #       resolution you'll want to attempt on the pi

while not done:

	if not os.path.isfile(turn_off_face_fname):
		webcam.release()
		done=True
		exit()

	aframe = webcam.read()[1]
	cv2.imwrite("/mnt/ramdisk/image.jpg",aframe)
	time.sleep(0.1)
	print "a"

