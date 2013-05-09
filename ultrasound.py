# Module: ultrasound.py
# This module can be used to operate an HC-SR04 ultrasonic sensor
# from a raspberry pi GPIO.

import time
import RPi.GPIO as GPIO

# setup which pins are which
TRIG = 8
ECHO = 10

# set the trigger pulse length and timeouts
pulsetrigger = 0.0001 # Trigger duration in seconds
timeout = 2100        # Length of time for timeout

def configure(trigger, echo):
    TRIG = trigger
    ECHO = echo
    GPIO.setup(TRIG, GPIO.OUT)
    GPIO.setup(ECHO, GPIO.IN)

def fire_trigger():
    # Set trigger high for 0.0001s then drop it low
    GPIO.output(TRIG, True)
    time.sleep(pulsetrigger)
    GPIO.output(TRIG, False)

def wait_for_echo(desired_state):
    countdown = timeout
    while (GPIO.input(ECHO) != desired_state and countdown > 0):
        countdown = countdown - 1
    return (countdown > 0) # Return true if success, false if timeout

def measure_time():
    # Fire the trigger to set the whole thing in motion
    fire_trigger()

    # Check that the echo goes high....
    if wait_for_echo(1):
        # Start the timer and wait for the echo to go low
        echo_start = time.time()
        if wait_for_echo(0):
            # Stop the timer
            echo_end = time.time()
            return echo_end - echo_start
        else:
            print "Timeout 2"
            return -1
    else:
        print "Timeout 1"
        return -1
    
def measure_average_time():
    count = 1
    total_time = 0
    while(count <= 3):
        total_time = total_time + measure_time()
        time.sleep(0.1)
        count = count + 1
    return total_time / 3
        
def distance_cm():
    time = measure_average_time()
    if time < 0:
        return -1
    else:
        return time * (1000000 / 58)


if __name__ == "__main__":
    print "Starting ultrasound test"
    # Set up the GPIO board
    GPIO.setmode(GPIO.BOARD)

    # Tell the Pi which pins the ultrasound is on
    configure(TRIG, ECHO)

    try:
        while True:
            distance = distance_cm()
            if distance < 0:
                print "Timeout"
            else:
                print "Distance = %.0f cm" % (int(round(distance)))
            time.sleep(2)

    except KeyboardInterrupt:
        print "Stopping"
        GPIO.cleanup()
        
    
