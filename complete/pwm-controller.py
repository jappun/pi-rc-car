import time
import RPi.GPIO as GPIO
from pyPS4Controller.controller import Controller 

## STEP 1: tell our computer what motors are connected to which pins
GPIO.setmode(GPIO.BCM) # or is it supposed to be GPIO.BOARD?

## TODO: CHANGE THIS FILE TO USE PWM FOR THE OLDER GRADES.
GPIO.setup(4, GPIO.OUT) # left motor 
GPIO.setup(5, GPIO.OUT) # right motor 
GPIO.setup(22, GPIO.OUT) # back wheels go forward
GPIO.setup(23, GPIO.OUT) # back wheels go backward

class MyController(Controller):

    # here, think of "self" as the physical PS4 controller,
    def __init__(self, back_wheels, left, right):
        self.back_wheels = tuple(back_wheels)
        self.forwards = back_wheels[0]
        self.backwards = back_wheels[1]
        self.left = left
        self.right = right
        Controller.__init__(self)

    # what do you think this code does?
    def on_x_press(self):
       GPIO.output(self.backwards, False)
       GPIO.output(self.forwards, True)
    
    # stop the car. which motor should you turn off?
    def on_x_release(self):
        GPIO.output(self.forwards, False)

    # move backwards in a straight line. which motor should we turn on?
    def on_square_press(self):
        GPIO.output(self.forwards, False)
        GPIO.output(self.backwards, True)

    # what do you think this code does?
    def on_square_release(self):
        GPIO.output(self.backwards, False)

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
controller.listen()