#!/usr/bin/python

# we import necessary external libraries
import RPi.GPIO as GPIO
import time

# defining stepper motor sequence (found in documentation
#   http://www.4tronix.co.uk/arduino/Stepper-Motors.php)
step_sequence = [[1,0,0,1],
                 [1,0,0,0],
                 [1,1,0,0],
                 [0,1,0,0],
                 [0,1,1,0],
                 [0,0,1,0],
                 [0,0,1,1],
                 [0,0,0,1]]

# we can't send steps too fast, the motor needs time to process them, so we
#   need to sleep a little between steps. you can play with this value to make
#   the motor slower or faster.
sleep_between_steps = 0.002 # seconds

# which GPIO pins are the stepper motors are hooked up to
motor_left_pins = [12,16,20,21]
motor_right_pins = [6,13,19,26]

# we need to keep track of which step the motors are at so we can properly
#   iterate through the stepper motor sequence.
motor_left_step_counter = 0
motor_right_step_counter = 0

GPIO.setmode( GPIO.BCM )
for gpio_pin in motor_left_pins:
    GPIO.setup( gpio_pin, GPIO.OUT )

for gpio_pin in motor_right_pins:
    GPIO.setup( gpio_pin, GPIO.OUT )

# used to rotate the left motor
#   number_of_steps: how many steps to take
#   direction: True for clockwise, False for counterclockwise
def actuate_left_motor( number_of_steps, direction ):
    global motor_left_step_counter

    # if somehow, the motor isn't turning in the right direction, uncomment this logic to reverse the direction
    # direction = not direction

    for i in range(0, number_of_steps):
        for pin in range(0, len(motor_left_pins)):
            GPIO.output( motor_left_pins[pin], step_sequence[motor_left_step_counter][pin] )
        if direction==True:
            motor_left_step_counter = (motor_left_step_counter - 1) % 8
        elif direction==False:
            motor_left_step_counter = (motor_left_step_counter + 1) % 8
        else: # defensive programming
            print "uh oh... direction should *always* be either True or False"

        time.sleep( sleep_between_steps )

def actuate_right_motor( number_of_steps, direction ):
    global motor_right_step_counter

    # if somehow, the motor isn't turning in the right direction, uncomment this logic to reverse the direction
    # direction = not direction

    for i in range(0, number_of_steps):
        for pin in range(0, len(motor_right_pins)):
            GPIO.output( motor_right_pins[pin], step_sequence[motor_right_step_counter][pin] )
        if direction==True:
            motor_right_step_counter = (motor_right_step_counter - 1) % 8
        elif direction==False:
            motor_right_step_counter = (motor_right_step_counter + 1) % 8
        else: # defensive programming
            print "uh oh... direction should *always* be either True or False"

        time.sleep( sleep_between_steps )
