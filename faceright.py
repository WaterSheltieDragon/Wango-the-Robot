import time
import maestro
# servo 0 is left/right
# servo 1 is up/down
try:
  servo = maestro.Controller()

  servo.setRange(0,3000,8200)
  servo.setRange(1,4000,8000)

  # about 5 clicks per full motion
  # 1040 for left/right  + is left, - is right.
  # 800 for up/down  + is up, - is down.
  x = servo.getPosition(0) - 1040

  servo.setAccel(0,6)
  servo.setTarget(0,x)

finally:
  servo.close

