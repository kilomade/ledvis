#!/usr/bin/env python3

# Test code for using interrupts
#
#
#

import signal
import sys
import RPi.GPIO as GPIO

try:
    import utils.config
except:
    print(e)
    
bus=None

def speed_adj_down(interupt_pin):
    print("Speed adj down triggered")

def speed_adj_up(interupt_pin):
    print("Speed adj up triggered")

def speed_adj_default(interupt_pin):
    print("Speed adj default triggered")

def brightness_adj_default(interupt_pin):
    print("Brightness adj default triggered")

def brightness_adj_up(interupt_pin):
    print("Brightness adj up triggered")

def brightness_adj_down(interrupt_pin):
    print("Brightness adj down triggered")

def turn_off_lights(interrupt_pin):
    print("Lights off triggered")

def mode_change_up_button_pressed(interrupt_pin):
    print("Mode change up triggered")

def mode_change_down_button_pressed(interrupt_pin):
    print("Mode change down triggered")

def default_mode_button_pressed(interrupt_pin):
    print("Mode default triggered")

def signal_handler(sig, frame):
    GPIO.cleanup()
    sys.exit(0)

if __name__ == '__main__':
    GPIO.setmode(GPIO.BCM)
    
    DEFAULT_MODE     = 16
    MODE_UP          = 12
    MODE_DOWN        = 1
    TURN_OFF         = 21
    TURN_ON          = 20
    BRIGHTNESS_UP    = 8
    BRIGHTNESS_DOWN  = 25
    BRIGHTNESS_DEF   = 7
    SPEED_ADJ_UP     = 23
    SPEED_ADJ_DOWN   = 18
    SPEED_DEF        = 24

    GPIO.setup(DEFAULT_MODE, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(MODE_UP, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(MODE_DOWN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(TURN_OFF, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(BRIGHTNESS_UP, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(BRIGHTNESS_DOWN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(BRIGHTNESS_DEF, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(SPEED_ADJ_UP, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(SPEED_ADJ_DOWN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(SPEED_DEF, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    GPIO.add_event_detect(DEFAULT_MODE, GPIO.BOTH, callback=default_mode_button_pressed, bouncetime=50)
    GPIO.add_event_detect(MODE_UP, GPIO.BOTH, callback=mode_change_up_button_pressed, bouncetime=50)
    GPIO.add_event_detect(MODE_DOWN, GPIO.BOTH, callback=mode_change_down_button_pressed, bouncetime=50)
    GPIO.add_event_detect(TURN_OFF, GPIO.BOTH, callback=turn_off_lights, bouncetime=50)
    GPIO.add_event_detect(BRIGHTNESS_UP, GPIO.BOTH, callback=brightness_adj_up, bouncetime=50)
    GPIO.add_event_detect(BRIGHTNESS_DOWN, GPIO.BOTH, callback=brightness_adj_down, bouncetime=50)
    GPIO.add_event_detect(BRIGHTNESS_DEF, GPIO.BOTH, callback=brightness_adj_default, bouncetime=50)
    GPIO.add_event_detect(SPEED_ADJ_DOWN, GPIO.BOTH, callback=speed_adj_down, bouncetime=50)
    GPIO.add_event_detect(SPEED_ADJ_UP, GPIO.BOTH, callback=speed_adj_up, bouncetime=50)
    GPIO.add_event_detect(SPEED_DEF, GPIO.BOTH, callback=speed_adj_default, bouncetime=50)

    signal.signal(signal.SIGINT, signal_handler)
    signal.pause()
    # print out a message and wait for keyboard input before
    # exiting the program