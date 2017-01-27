from multiprocessing import Process, Queue
import time
import cv2
import maestro
import os.path
import sys
import os
import pygame

turn_off_face_fname = "/var/www/html/turn_off_face.txt"

# Upper limit
_Servo1UL = 8000
_Servo0UL = 8200

# Lower Limit
_Servo1LL = 4000
_Servo0LL = 3000

continueleft = 0
continueright = 0
hit_end = False
bounce = True         

prev_faceFound = False
faceFound = False


face = [0,0,0,0]	# This will hold the array that OpenCV returns when it finds a face: (makes a rectangle)
Cface = [0,0]		# Center of the face: a point calculated from the above variable
lastface = 0		# int 1-3 used to speed up detection. The script is looking for a right profile face,-
			# 	a left profile face, or a frontal face; rather than searching for all three every time,-
			# 	it uses this variable to remember which is last saw: and looks for that again. If it-
			# 	doesn't find it, it's set back to zero and on the next loop it will search for all three.-
			# 	This basically tripples the detect time so long as the face hasn't moved much.

Servo0CP = Queue()	# Servo zero current position, sent by subprocess and read by main process
Servo1CP = Queue()	# Servo one current position, sent by subprocess and read by main process
Servo0DP = Queue()	# Servo zero desired position, sent by main and read by subprocess
Servo1DP = Queue()	# Servo one desired position, sent by main and read by subprocess
Servo0S = Queue()	# Servo zero speed, sent by main and read by subprocess
Servo1S = Queue()	# Servo one speed, sent by main and read by subprocess

def draw_rect(img, rect, color):
	#for x1, y1, x2, y2 in rects:
	x1,y1,w,h = rect
	x2 = x1+w
	y2 = y1+h
	cv2.rectangle(img, (x1, y1), (x2, y2), color, 2)


def P0():	# Process 0 controlles servo0
	speed = .1		# Here we set some defaults:
	try:
		_Servo0CP = servo.getPosition(0)		# by making the current position and desired position unequal,-
		_Servo0DP = (_Servo0UL - _Servo0LL)/2+_Servo0LL		# 	we can be sure we know where the servo really is. (or will be soon)
		while True:
			time.sleep(speed)
			if Servo0CP.empty():			# Constantly update Servo0CP in case the main process needs-
				Servo0CP.put(_Servo0CP)		# 	to read it
			if not Servo0DP.empty():		# Constantly read read Servo0DP in case the main process-
				_Servo0DP = Servo0DP.get()	#	has updated it
			if not Servo0S.empty():			# Constantly read read Servo0S in case the main process-
				_Servo0S = Servo0S.get()	# 	has updated it, the higher the speed value, the shorter-
				speed = .1 / _Servo0S		# 	the wait between loops will be, so the servo moves faster
			if not servo.getMovingState() or _Servo0LL == _Servo0LL or _Servo0LL == _Servo0LL:
				if _Servo0CP < _Servo0DP:					# if Servo0CP less than Servo0DP
					_Servo0CP += 10						# incriment Servo0CP up by one
					Servo0CP.put(_Servo0CP)					# move the servo that little bit
					servo.setTarget(0,_Servo0CP)	#
					if not Servo0CP.empty():				# throw away the old Servo0CP value,-
						trash = Servo0CP.get()				# 	it's no longer relevent
				if _Servo0CP > _Servo0DP:					# if Servo0CP greater than Servo0DP
					_Servo0CP -= 10						# incriment Servo0CP down by one
					Servo0CP.put(_Servo0CP)					# move the servo that little bit
					servo.setTarget(0,_Servo0CP)	#
					if not Servo0CP.empty():				# throw away the old Servo0CP value,-
						trash = Servo0CP.get()				# 	it's no longer relevent
				if _Servo0CP == _Servo0DP:	        # if all is good,-
					_Servo0S = 1		        # slow the speed; no need to eat CPU just waiting
	finally:
		print "p0 servo error"
			

def P1():	# Process 1 controlles servo 1 using same logic as above
	speed = .1
	try:
		_Servo1CP = servo.getPosition(1)
		_Servo1DP = (_Servo1UL - _Servo1LL)/2+_Servo1LL
		while True:
			time.sleep(speed)
			if Servo1CP.empty():
				Servo1CP.put(_Servo1CP)
			if not Servo1DP.empty():
				_Servo1DP = Servo1DP.get()
			if not Servo1S.empty():
				_Servo1S = Servo1S.get()
				speed = .1 / _Servo1S
			if servo.getMovingState() or _Servo1CP == _Servo1LL or _Servo1CP == _Servo1UL:
				if _Servo1CP < _Servo1DP:
					_Servo1CP += 30
					Servo1CP.put(_Servo1CP)
					servo.setTarget(1,_Servo1CP)
					if not Servo1CP.empty():
						trash = Servo1CP.get()
				if _Servo1CP > _Servo1DP:
					_Servo1CP -= 30
					Servo1CP.put(_Servo1CP)
					servo.setTarget(1,_Servo1CP)
					if not Servo1CP.empty():
						trash = Servo1CP.get()
				if _Servo1CP == _Servo1DP:
					_Servo1S = 1
	finally:
		print "p1 servo error"

def CamRight( distance, speed ):		# To move right, we are provided a distance to move and a speed to move.
	global _Servo0CP			# We Global it so  everyone is on the same page about where the servo is...
	global hit_end
	distance = distance * 2
	speed = speed * 2
	if not Servo0CP.empty():		# Read it's current position given by the subprocess(if it's avalible)-
		_Servo0CP = Servo0CP.get()	# 	and set the main process global variable.
	_Servo0DP = _Servo0CP + distance	# The desired position is the current position + the distance to move.
	if _Servo0DP >= _Servo0UL:		# But if you are told to move further than the servo is built go...
		_Servo0DP = _Servo0UL		# Only move AS far as the servo is built to go.
		hit_end = True
	else:
		hit_end = False
	Servo0DP.put(_Servo0DP)			# Send the new desired position to the subprocess
	Servo0S.put(speed)			# Send the new speed to the subprocess
	return;

def CamLeft(distance, speed):			# Same logic as above
	global _Servo0CP
	global hit_end
	distance = distance * 2
	speed = speed * 2
	if not Servo0CP.empty():
		_Servo0CP = Servo0CP.get()
	_Servo0DP = _Servo0CP - distance
	if _Servo0DP <= _Servo0LL:
		_Servo0DP = _Servo0LL
		hit_end = True
	else:
		hit_end = False
	Servo0DP.put(_Servo0DP)
	Servo0S.put(speed)
	return;


def CamDown(distance, speed):			# Same logic as above
	global _Servo1CP
	if not Servo1CP.empty():
		_Servo1CP = Servo1CP.get()
	_Servo1DP = _Servo1CP + distance
	if _Servo1DP > _Servo1UL:
		_Servo1DP = _Servo1UL
	Servo1DP.put(_Servo1DP)
	Servo1S.put(speed)
	return;


def CamUp(distance, speed):			# Same logic as above
	global _Servo1CP
	if not Servo1CP.empty():
		_Servo1CP = Servo1CP.get()
	_Servo1DP = _Servo1CP - distance
	if _Servo1DP < _Servo1LL:
		_Servo1DP = _Servo1LL
	Servo1DP.put(_Servo1DP)
	Servo1S.put(speed)
	return;
#============================================================================================================


if __name__ == '__main__':

	
	try:
		import socket
		s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
		## Create an abstract socket, by prefixing it with null. 
		s.bind( '\0find_face_lock') 

	except socket.error, e:
		error_code = e.args[0]
		error_string = e.args[1]
		print "Process already running (%d:%s ). Exiting" % ( error_code, error_string) 
		sys.exit (0)

	else:
		try:
			servo = maestro.Controller()
			pygame.init()
			pygame.mixer.init()
			pygame.mixer.music.load("/var/www/html/beep6.mp3")
			pygame.mixer.music.set_volume(0.1)
			pygame.mixer.music.play()
			while pygame.mixer.music.get_busy(): 
				pygame.time.Clock().tick(10)
			pygame.mixer.music.load("/var/www/html/hello.mp3")
			pygame.mixer.music.set_volume(0.1)

			servo.setAccel(1,8)
			servo.setAccel(0,8)
			servo.setRange(0,_Servo0LL,_Servo0UL)
			servo.setRange(1,_Servo1LL,_Servo1UL)
			servo.setTarget(0,(_Servo0UL - _Servo0LL)/2+_Servo0LL)
			servo.setTarget(1,(_Servo1UL - _Servo1LL)/2+_Servo1LL)


			webcam = cv2.VideoCapture(-1)                           # Get ready to start getting images from the webcam
			webcam.set(cv2.cv.CV_CAP_PROP_FRAME_WIDTH, 320)         # I have found this to be about the highest-
			webcam.set(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT, 240)        #       resolution you'll want to attempt on the pi

			frontalface = cv2.CascadeClassifier("haarcascade_frontalface_alt2.xml")         # frontal face pattern detection
			profileface = cv2.CascadeClassifier("haarcascade_profileface.xml")              # side face pattern detection

			p_p0 = Process(target=P0, args=())	# Start the subprocesses
			p_p0.start()
			p_p1 = Process(target=P1, args=())	#
			p_p1.start()
			time.sleep(1)				# Wait for them to start
			print p_p0, p_p0.is_alive()


			done = False
			cnt = 0
			while not done:
				
				time.sleep(0.1)
				
				prev_faceFound = faceFound
				faceFound = False	# This variable is set to true if, on THIS loop a face has already been found
							# We search for a face three diffrent ways, and if we have found one already-
							# there is no reason to keep looking.
				print "."
				if os.path.isfile(turn_off_face_fname):
					try:
						print "Closing servos."
						Servo0CP.close()
						Servo1CP.close()
						Servo0DP.close()
						Servo1DP.close()
						Servo0S.close()
						Servo1S.close()
						p_p0.terminate()
						time.sleep(0.1)
						p_p1.terminate()
						time.sleep(0.1)
						p_p0.join()
						p_p1.join()
						webcam.release()
						servo.close()
						print "Completed normal shutdown of PiFace."
					finally:
						print "Done."

					exit()
					done = True

				if not faceFound and not done:
					if lastface == 0 or lastface == 1:
						aframe = webcam.read()[1]	# there seems to be an issue in OpenCV or V4L or my webcam-
						aframe = webcam.read()[1]	# 	driver, I'm not sure which, but if you wait too long,
						aframe = webcam.read()[1]	#	the webcam consistantly gets exactly five frames behind-
						aframe = webcam.read()[1]	#	realtime. So we just grab a frame five times to ensure-
						aframe = webcam.read()[1]	#	we have the most up-to-date image.
						fface = frontalface.detectMultiScale(aframe,1.3,4,(cv2.cv.CV_HAAR_DO_CANNY_PRUNING + cv2.cv.CV_HAAR_FIND_BIGGEST_OBJECT + cv2.cv.CV_HAAR_DO_ROUGH_SEARCH),(60,60))
						if fface != ():			# if we found a frontal face...
							lastface = 1		# set lastface 1 (so next loop we will only look for a frontface)
							for f in fface:		# f in fface is an array with a rectangle representing a face
								faceFound = True
								face = f

					if not faceFound:		# if no face was found...-
						lastface = 0		# 	the next loop needs to know
						face = [0,0,0,0]	# so that it doesn't think the face is still where it was last loop
						
					if bounce and faceFound:
						bounce = False
						print "Found you."
						pygame.mixer.music.play()
						while pygame.mixer.music.get_busy(): 
							pygame.time.Clock().tick(10)

					x,y,w,h = face
					Cface = [(w/2+x),(h/2+y)]	# we are given an x,y corner point and a width and height, we need the center

					img_out = aframe.copy()

					if Cface[0] != 0:		# if the Center of the face is not zero (meaning no face was found)

						draw_rect(img_out,face,(0,255,0))

						print str(Cface[0]) + "," + str(Cface[1])
						continueleft = 0
						continueright = 0

						if Cface[0] > 220:	# The camera is moved diffrent distances and speeds depending on how far away-
							print "far right"
							CamLeft(200,3)	#	from the center of that axis it detects a face
							continueleft = 3
						elif Cface[0] > 200:	#
							print "middle right"
							CamLeft(50,2)	#
							continueleft = 2
						elif Cface[0] > 180:	#
							print "little right"
							CamLeft(20,1)	#
							continueleft = 1

						if Cface[0] < 100:	# and diffrent dirrections depending on what side of center if finds a face.
							print "far left"
							CamRight(200,3)
							continueright = 3
						elif Cface[0] < 120:
							print "middle left"
							CamRight(50,2)
							continueright = 2
						elif Cface[0] < 140:
							print "little left"
							CamRight(20,1)
							continueright = 1

						if Cface[1] > 170:	# and moves diffrent servos depending on what axis we are talking about.
							CamUp(300,1)
						elif Cface[1] > 150:
							CamUp(300,2)
						elif Cface[1] > 140:
							CamUp(200,3)

						if Cface[1] < 80:
							CamDown(400,3)
						elif Cface[1] < 90:
							CamDown(300,2)
						elif Cface[1] < 110:
							CamDown(200,1)

					else:
						
						if continueleft > 0:
							CamLeft(200,continueleft)
							if hit_end:
								continueleft = 0
								continueright = 3
								hit_end = False
								bounce = True
								print "bounce"
						if continueright > 0:
							CamRight(200,continueright)
							if hit_end:
								continueleft = 3
								continueright = 0
								hit_end = False
								bounce = True
								print "bounce"

						
					cnt = cnt + 1
					if cnt == 10:
						cnt = 0
						cv2.imwrite("/mnt/ramdisk/image.jpg",img_out)
		except:
			print("Unexpected error:", sys.exc_info()[0])
			print "Closing servos."
			Servo0CP.close()
			Servo1CP.close()
			Servo0DP.close()
			Servo1DP.close()
			Servo0S.close()
			Servo1S.close()
			p_p0.terminate()
			time.sleep(0.1)
			p_p1.terminate()
			time.sleep(0.1)
			p_p0.join()
			p_p1.join()
			webcam.release()
			servo.close()
			print "Completed normal shutdown of PiFace."
