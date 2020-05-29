#!/usr/bin/env python3

# Test code for using interrupts
#
#
#

import signal
import sys
import RPi.GPIO as GPIO
import config

try:
    from IOPi import IOPi
except ImportError:
    print("Failed to import IOPi from python system path")
    print("Importing from parent folder instead")
    try:
        import sys
        sys.path.append("..")
        from IOPi import IOPi
    except ImportError:
        raise ImportError(
            "Failed to import library from parent folder")

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


if __name__ == '__main__':
    global bus

    bus = IOPi(0x20)
    bus.set_port_pullups(0, 0xFF)
    bus.set_port_direction(0, 0xFF)
    bus.invert_port(0, 0xFF)
    bus.set_interrupt_polarity(0)
    bus.mirror_interrupts(0)
    bus.set_interrupt_defaults(0, 0x00)
    bus.set_interrupt_type(0, 0xFF)
    bus.set_interrupt_on_port(0, 0xFF)
    bus.reset_interrupts()
    GPIO.setmode(GPIO.BCM)

    # Set up GPIO 23 as an input. The pull-up resistor is disabled as the
    # level shifter will act as a pull-up.
    GPIO.setup(DEFAULT_MODE, GPIO.IN, pull_up_down=GPIO.PUD_OFF)
    GPIO.setup(MODE_UP, GPIO.IN, pull_up_down=GPIO.PUD_OFF)
    GPIO.setup(MODE_DOWN, GPIO.IN, pull_up_down=GPIO.PUD_OFF)
    GPIO.setup(TURN_OFF, GPIO.IN, pull_up_down=GPIO.PUD_OFF)
    GPIO.setup(BRIGHTNESS_UP, GPIO.IN, pull_up_down=GPIO.PUD_OFF)
    GPIO.setup(BRIGHTNESS_DOWN, GPIO.IN, pull_up_down=GPIO.PUD_OFF)
    GPIO.setup(BRIGHTNESS_DEF, GPIO.IN, pull_up_down=GPIO.PUD_OFF)
    GPIO.setup(SPEED_ADJ_UP, GPIO.IN, pull_up_down=GPIO.PUD_OFF)
    GPIO.setup(SPEED_ADJ_DOWN, GPIO.IN, pull_up_down=GPIO.PUD_OFF)
    GPIO.setup(SPEED_DEF, GPIO.IN, pull_up_down=GPIO.PUD_OFF)

    # when a falling edge is detected on GPIO 23 the function
    # button_pressed will be run

    GPIO.add_event_detect(DEFAULT_MODE, GPIO.FALLING, callback=default_mode_button_pressed)
    GPIO.add_event_detect(MODE_UP, GPIO.FALLING, callback=mode_change_up_button_pressed)
    GPIO.add_event_detect(MODE_DOWN, GPIO.FALLING, callback=mode_change_down_button_pressed)
    GPIO.add_event_detect(TURN_OFF, GPIO.FALLING, callback=turn_off_lights)
    GPIO.add_event_detect(BRIGHTNESS_UP, GPIO.FALLING, callback=brightness_adj_up)
    GPIO.add_event_detect(BRIGHTNESS_DOWN, GPIO.FALLING, callback=brightness_adj_down)
    GPIO.add_event_detect(BRIGHTNESS_DEF, GPIO.FALLING, callback=brightness_adj_default)
    GPIO.add_event_detect(SPEED_ADJ_DOWN, GPIO.FALLING, callback=speed_adj_down)
    GPIO.add_event_detect(SPEED_ADJ_UP, GPIO.FALLING, callback=speed_adj_up)
    GPIO.add_event_detect(SPEED_DEF, GPIO.FALLING, callback=speed_adj_default)
    # print out a message and wait for keyboard input before
    # exiting the program