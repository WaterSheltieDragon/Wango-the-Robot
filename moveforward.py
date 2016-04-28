import time
from pololu_drv8835_rpi import motors, MAX_SPEED

# Set up sequences of motor speeds.
forward_speeds = list(range(0, MAX_SPEED , 2)) + list(range(MAX_SPEED,0,-2)) + [0]

reverse_speeds = list(range(0, -MAX_SPEED , -2)) + list(range(-MAX_SPEED,0,+2)) +  [0]

try:
    motors.setSpeeds(0, 0)

    for s in forward_speeds:
        motors.motor1.setSpeed(-s)
        motors.motor2.setSpeed(s)
        time.sleep(0.005)


finally:
  # Stop the motors, even if there is an exception
  # or the user presses Ctrl+C to kill the process.
  motors.setSpeeds(0, 0)

