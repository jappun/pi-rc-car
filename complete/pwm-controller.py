import time
import RPi.GPIO as GPIO
from pyPS4Controller.controller import Controller 

## STEP 1: tell our computer what motors are connected to which pins
GPIO.setmode(GPIO.BCM) # or is it supposed to be GPIO.BOARD?

GPIO.setup(4, GPIO.OUT) # left motor 
GPIO.setup(5, GPIO.OUT) # right motor 
GPIO.setup(22, GPIO.OUT) # back wheels go forward
GPIO.setup(23, GPIO.OUT) # back wheels go backward

# older students will learn about PWM for forward/back.
# as a challenge they can implement it for turning too

forward_speed = GPIO.PWM(22, 100) # sending all possible power to the motor when we go forward
backward_speed = GPIO.PWM(23, 100) # sending half the power to the motor when we got forward
# start both at 0
forward_speed.start(0)
backward_speed.start(0)

class MyController(Controller):

    # STEP 2: make a digital version of our controller
    # this part prob do a high level walk thru of constructor

    # here, think of "self" as the physical PS4 controller,
    def __init__(self, back_wheels, left, right):
        self.back_wheels = tuple(back_wheels)
        self.forwards = back_wheels[0]
        self.backwards = back_wheels[1]
        self.left = left
        self.right = right
        Controller.__init__(self)

    # STEP 3: add actions to buttons

    # what do you think this code does?
    def on_R3_up(self, value):
       speed = abs(value) / 32767 * 100 # normalization i got from claude bc i wasn't sure what the ps4 joystick maps to can we check
       backward_speed.ChangeDutyCycle(0)
       forward_speed.ChangeDutyCycle(speed)
    
    # stop the car. which motor should you turn off?
    def on_R3_y_at_rest(self):
        backward_speed.ChangeDutyCycle(0)
        forward_speed.ChangeDutyCycle(0)

    # move backwards in a straight line. which motor should we turn on?
    def on_R3_down(self, value):
       speed = abs(value) / 32767 * 100 # normalization i got from claude bc i wasn't sure what the ps4 joystick maps to can we check
       forward_speed.ChangeDutyCycle(0)
       backward_speed.ChangeDutyCycle(speed)

    # spin the right wheel to turn left
    def on_left_arrow_press(self):
        GPIO.output(self.right, True)

    # stop turning left
    def on_left_arrow_release(self):
        GPIO.output(self.right, False)

    # spin the left wheel to turn right
    def on_right_arrow_press(self):
        GPIO.output(self.left, True)
    
    # stop turning right
    def on_right_arrow_release(self):
        GPIO.output(self.left, False)

controller = MyController((22,23), 4, 5, interface="/dev/input/js0", connecting_using_ds4drv=False)
try:
    controller.listen()
finally: 
    GPIO.cleanup()