import time
import maestro
# servo 0 is left/right
# servo 1 is up/down

# about 5 clicks per full motion
# 1040 for left/right  + is left, - is right.
# 800 for up/down  + is up, - is down.
  
try:
  servo = maestro.Controller()

  servo.setRange(0,3000,8200)
  servo.setRange(1,4000,8000)
  servo.setAccel(1,6)
  
  # open channel 2 file.  2 = servos, 1 = dc motors
  f = open('/etc/ramdisk/cmd2.txt', 'r+')
  cmd = f.readline()

  if cmd == "down":
    x = servo.getPosition(1) - 800
    servo.setTarget(1,x)
  elif cmd == "up":
    x = servo.getPosition(1) + 800
    servo.setTarget(1,x)

finally:
  servo.close
