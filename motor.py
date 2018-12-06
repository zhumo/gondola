# Import needed modules
import time
import RPi.GPIO as GPIO
import random
import web
#### o_o
import stepper
#### -_-

led = 4     # connect the LED to this pin on the GPIO
pir = 17      # connect the PIR motion detector to this pin on the GPIO

STEPS_PER_UNIT = 330

# Set the mode for the pin
GPIO.setmode( GPIO.BCM )
# Set our LED, pin 4, to output
GPIO.setup( led, GPIO.OUT )
# Set out PIR motion detector, pin 17 to input
GPIO.setup( pir, GPIO.IN )

servo = 25
pen_down_duty_cycle = 10
pen_up_duty_cycle = 12
# Set Servo motor to output
GPIO.setup( servo, GPIO.OUT )
# not sure what this is anymore, look into
pwm = GPIO.PWM( servo, 50 )
# we always start with the pen up
pen_sleep = 2
pwm.start( pen_up_duty_cycle )
time.sleep(pen_sleep)
pwm.ChangeDutyCycle(0)

def pen_down():
    global pwm
    print "> pen down"
    pwm.ChangeDutyCycle( pen_down_duty_cycle )
    time.sleep(pen_sleep)
    pwm.ChangeDutyCycle(0)

def pen_up():
    global pwm
    print "> pen up"
    pwm.ChangeDutyCycle( pen_up_duty_cycle )
    time.sleep(pen_sleep)
    pwm.ChangeDutyCycle(0)

def led_on():
    print "> LED on"
    GPIO.output( led, 1 )

def led_off():
    print "> LED off"
    GPIO.output( led, 0 )

#### o_o
stepper_left_total_steps = 0

def stepper_left_turn_clockwise( steps ):
    steps = int(steps)
    print "> stepper left " + str(steps) + " steps clockwise"
    stepper.actuate_left_motor( steps, True )
    global stepper_left_total_steps
    stepper_left_total_steps += steps
    return "Stepper motor left took " + str(stepper_left_total_steps) + " steps total"
def stepper_left_turn_counterclockwise( steps ):
    steps = int(steps)
    print "> stepper left " + str(steps) + " steps counter-clockwise"
    stepper.actuate_left_motor( steps, False )
    global stepper_left_total_steps
    stepper_left_total_steps -= steps
    return "Stepper motor left took " + str(stepper_left_total_steps) + " steps total"

def stepper_right_turn_clockwise( steps ):
    steps = int(steps)
    print "> stepper right " + str(steps) + " steps clockwise"
    stepper.actuate_right_motor( steps, True )
    global stepper_right_total_steps
    stepper_right_total_steps += steps
    return "Stepper motor right took " + str(stepper_right_total_steps) + " steps total"

def stepper_right_turn_counterclockwise( steps ):
    steps = int(steps)
    print "> stepper right " + str(steps) + " steps counter-clockwise"
    stepper.actuate_right_motor( steps, False )
    global stepper_right_total_steps
    stepper_right_total_steps -= steps
    return "Stepper motor right took " + str(stepper_right_total_steps) + " steps total"
#### -_-

def get_l(x,y):
    return (x**2 + (100-y)**2)**0.5
def get_r(x,y):
    return ((100-x)**2 + (100-y)**2)**0.5

def get_l_diff(x_origin, y_origin, x_destination, y_destination):
    return get_l(x_destination, y_destination) - get_l(x_origin, y_origin)

def get_r_diff(x_origin, y_origin, x_destination, y_destination):
    return get_r(x_destination, y_destination) - get_r(x_origin, y_origin)

def units_to_steps(units):
    return int(round(units * STEPS_PER_UNIT))

def from_go_to( x_origin, y_origin, x_destination, y_destination ):
    x_origin = float( x_origin )
    y_origin = float( y_origin )
    x_destination = float( x_destination )
    y_destination = float( y_destination )
    l_steps = units_to_steps( get_l_diff(x_origin, y_origin, x_destination, y_destination) )
    r_steps = units_to_steps( get_r_diff(x_origin, y_origin, x_destination, y_destination) )
    l_direction = False
    if l_steps<0:
        l_direction = True
        l_steps = abs(l_steps)
    r_direction = True
    if r_steps<0:
        r_direction = False
        r_steps = abs(r_steps)
    steps_to_take = [] ;
    for i in range( l_steps ):
        steps_to_take.append( "l" )
    for i in range( r_steps ):
        steps_to_take.append( "r" )
    random.shuffle( steps_to_take )
    for i in range(len(steps_to_take)):
        if steps_to_take[i]=="l":
            stepper.actuate_left_motor( 1, l_direction )
        else:
            stepper.actuate_right_motor( 1, r_direction )

x_current = 50.0
y_current = 50.0
def go_to( x_destination, y_destination ):
    global x_current, y_current

    from_go_to( x_current, y_current, x_destination, y_destination )
    x_current = x_destination
    y_current = y_destination

def parse_go_to_code( go_to_code ):
    print "> parse_go_to_code called"
    go_to_code = go_to_code.replace( " ", "" )
    go_to_code = go_to_code.lower()
    go_to_code = go_to_code.split( "\n" )
    for line in go_to_code:
        print ">   " + line
        line = line.split( "(" )
        if len(line)==2:
            command = line[0]
            params = line[1].replace( ")", "" ).split( "," )
            if command=="go_to" and len(params)==2:
                to_X = float( params[0] )
                to_Y = float( params[1] )
                go_to( to_X, to_Y )
            elif command=="pen_up":
                pen_up()
            elif command=="pen_down":
                pen_down()
            else:
                print ">   WARNING: can't parse line: " + "(".join( line )

try:
    web.server_start()
    web.register( "<button>Turn LED on</button>", led_on )
    web.register( "<button>Turn LED off</button>", led_off )
#### o_o
    web.arbitrary_html( "<br/>" )
    web.register( "<button>Stepper Left CW</button><input type=\"text\" placeholder=\"step_count\"/>", stepper_left_turn_clockwise )
    web.register( "<button>Stepper Left CCW</button><input type=\"text\" placeholder=\"step_count\"/>", stepper_left_turn_counterclockwise )

    web.arbitrary_html( "<br/>" )
    web.register( "<button>Stepper Right CW</button><input type=\"text\" placeholder=\"step_count\"/>", stepper_right_turn_clockwise )
    web.register( "<button>Stepper Right CCW</button><input type=\"text\" placeholder=\"step_count\"/>", stepper_right_turn_counterclockwise )

    web.arbitrary_html( "<br/>" )
    web.register( '<button>From Go To</button><input type="text" placeholder="origin_x"/><input type="text" placeholder="origin_y"/><input type="text" placeholder="destination_x"/><input type="text" placeholder="destination_y"/>', from_go_to )

    web.arbitrary_html( "<br/>" )
    web.register( '<button>Go To</button><input type="text" placeholder="destination_x"/><input type="text" placeholder="destination_y"/>', go_to )

    web.arbitrary_html( '<br/>' )
    web.register( '<button>Pen Up</button>', pen_up )
    web.register( '<button>Pen Down</button>', pen_down )

    web.arbitrary_html( '<br/>' )
    web.register( '<textarea cols="50" rows="24" onInput="draw_go_to_code(this.value, document.getElementById(\'canvas\'));"></textarea><canvas id="canvas" width="300" height="300"></canvas><button>Go!</button>', parse_go_to_code )
    
#### -_-
    motion_led_on = False
    while True:
        if GPIO.input(pir)==1:
            print "> motion detected"
            if motion_led_on==False:
                led_on()
                motion_led_on = True
        else:
            if motion_led_on==True:
                led_off()
                motion_led_on = False
        time.sleep( 0.5 )
except KeyboardInterrupt: # when ctrl+c is pressed, turn LED off & the infinite loop stops
    pass

# the program is finished, we put things back in their original state
print "> finishing"
web.server_stop()
led_off()
GPIO.cleanup()
