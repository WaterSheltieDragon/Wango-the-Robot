import time
from pololu_drv8835_rpi import motors, MAX_SPEED

try:
    motors.setSpeeds(0, 0)


finally:
  # Stop the motors, even if there is an exception
  # or the user presses Ctrl+C to kill the process.
  motors.setSpeeds(0, 0)

