# Import needed modules
import time
import RPi.GPIO as GPIO

led = 4     # connect the LED to this pin on the GPIO

# Import needed modules
import time
import RPi.GPIO as GPIO
#### o_o
import random
#### -_-

led = 4     # connect the LED to this pin on the GPIO

# Set the mode for the pin
GPIO.setmode( GPIO.BCM )
# Set our LED, pin 27, to output
GPIO.setup( led, GPIO.OUT )

#### o_o
LED_state = 0
try:
    for i in range(0, 100):
        time.sleep( random.random()/2 )
        if LED_state==0:
            print "on"
            GPIO.output( led, 1 )
            LED_state = 1
        elif LED_state==1:
            print "off"
            GPIO.output( led, 0 )
            LED_state = 0
        else:
            print "Something went horribly wrong, we should never reach this point."
            break
except KeyboardInterrupt:
    pass
#### -_-

# the program is finished, we put things back in their original state
GPIO.cleanup()
