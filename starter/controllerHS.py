import time
import RPi.GPIO as GPIO
from pyPS4Controller.controller import Controller 

## STEP 1: tell our computer what motors are connected to which pins
GPIO.setmode(GPIO.BCM) 

# front wheels
GPIO.setup(4, GPIO.OUT) #Front right wheel backwards in1
GPIO.setup(22, GPIO.OUT) #Front right wheel forwards in2
GPIO.setup(27, GPIO.OUT) #front left wheels forward in3 
GPIO.setup(23, GPIO.OUT) #front left wheels backward in4 

#back wheels
GPIO.setup(24, GPIO.OUT) #Back left wheel forward in1
GPIO.setup(25, GPIO.OUT) #Back left wheel backwards in2
GPIO.setup(5, GPIO.OUT) #Back right wheel forward in3 
GPIO.setup(6, GPIO.OUT) #Back right wheel backward in in4 

## STEP 2: Variables for wheel + direction to pin matching
f_right_forward = 22
f_right_backward = 4
f_left_forward = 27 
f_left_backward = 23

b_right_forward = 5
b_right_backward = 6
b_left_forward = 24
b_left_backward = 25

## TODO: Find which pins make the car go in specific direction
forward = (f_right_forward, f_left_forward, b_right_forward, b_left_forward)
backward = ()
right = ()
left = ()


class MyController(Controller):

    # STEP 3: make a digital version of our controller

    # here, think of "self" as the physical PS4 controller,
    def __init__(self, forward, backward, left, right, **kwargs):
        self.forwards = forward
        self.backwards = backward
        self.left = left
        self.right = right
        Controller.__init__(self, **kwargs)

    # STEP 4: add actions to the buttons
    # if we want to move forward when we press R2 we need to turn forward "on"
    def on_R2_press(self):
       GPIO.output(self.backwards, False)
       GPIO.output(self.forwards, True)
    
    # What does this code do?
    def on_R2_release(self):
        GPIO.output(self.forwards, False)

    ## TODO: move backwards in a straight line. which motor should we turn on?
    def on_L2_press(self):
        # Start code here

        return # remove when done writing

    ## TODO: stop the car from moving backwards. which motor do we turn off?
    def on_L2_release(self):
        # Start code here

        return # remove when done writing

    ## TODO: spin the right wheel to turn left
    def on_left_arrow_press(self):
        # Start code here

        return # remove when done writing

    ## TODO: stop turning right or left 
    def on_left_right_arrow_release(self):
        # Start code here

        return # remove when done writing


    ## TODO: spin the left wheel to turn right
    def on_right_arrow_press(self):
        # Start code here

        return # remove when done writing


# Creating a controller object to run
controller = MyController(forward, backward, left, right, interface="/dev/input/js0", connecting_using_ds4drv=False)

# Listen for button presses - and do the action based on the code above
controller.listen()