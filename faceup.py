import time
import maestro
# servo 0 is left/right
# servo 1 is up/down
try:
  servo = maestro.Controller()

  servo.setRange(1,4000,8000)

  # about 5 clicks per full motion
  # 1040 for left/right  + is left, - is right.
  # 800 for up/down  + is up, - is down.
  x = servo.getPosition(1) + 800

  servo.setAccel(1,6)
  servo.setTarget(1,x)

finally:
  servo.close

