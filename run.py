import time
from pololu_drv8835_rpi import motors, MAX_SPEED

# Set up sequences of motor speeds.
forward_speeds = list(range(0, MAX_SPEED , 2))
reverse_speeds = list(range(0, -MAX_SPEED , -2))


for s in forward_speeds:
        motors.motor1.setSpeed(-s)
        motors.motor2.setSpeed(s)
        time.sleep(0.005)



