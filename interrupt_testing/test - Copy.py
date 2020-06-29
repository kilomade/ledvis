#!/usr/bin/env python3

# Test code for using interrupts
#
#
#

import signal
import sys
import RPi.GPIO as GPIO
import wiringpi

try:
    import utils.config
except:
    print(e)

bus = None


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


def turn_on_lights(interrupt_pin):
    print("Lights on triggered")


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
    SPEED_ADJ_DOWN = 1
    SPEED_ADJ_UP = 4
    SPEED_DEF = 5
    BRIGHTNESS_DOWN = 6
    BRIGHTNESS_UP = 10
    BRIGHTNESS_DEF = 11
    MODE_DOWN = 31
    MODE_UP = 26
    DEFAULT_MODE = 27
    TURN_ON = 28
    TURN_OFF = 29

    wiringpi.wiringPiSetupGpio()
    wiringpi.pinMode(DEFAULT_MODE, wiringpi.GPIO.INPUT)
    wiringpi.pinMode(MODE_UP, wiringpi.GPIO.INPUT)
    wiringpi.pinMode(MODE_DOWN, wiringpi.GPIO.INPUT)
    wiringpi.pinMode(TURN_OFF, wiringpi.GPIO.INPUT)
    wiringpi.pinMode(TURN_ON, wiringpi.GPIO.INPUT)
    wiringpi.pinMode(BRIGHTNESS_UP, wiringpi.GPIO.INPUT)
    wiringpi.pinMode(BRIGHTNESS_DOWN, wiringpi.GPIO.INPUT)
    wiringpi.pinMode(BRIGHTNESS_DEF, wiringpi.GPIO.INPUT)
    wiringpi.pinMode(SPEED_ADJ_UP, wiringpi.GPIO.INPUT)
    wiringpi.pinMode(SPEED_ADJ_DOWN, wiringpi.GPIO.INPUT)
    wiringpi.pinMode(SPEED_DEF, wiringpi.GPIO.INPUT)

    wiringpi.pullUpDnControl(DEFAULT_MODE, wiringpi.GPIO.PUD_DOWN)
    wiringpi.pullUpDnControl(MODE_UP, wiringpi.GPIO.PUD_DOWN)
    wiringpi.pullUpDnControl(MODE_DOWN, wiringpi.GPIO.PUD_DOWN)
    wiringpi.pullUpDnControl(TURN_OFF, wiringpi.GPIO.PUD_DOWN)
    wiringpi.pullUpDnControl(TURN_ON, wiringpi.GPIO.PUD_DOWN)
    wiringpi.pullUpDnControl(BRIGHTNESS_UP, wiringpi.GPIO.PUD_DOWN)
    wiringpi.pullUpDnControl(BRIGHTNESS_DOWN, wiringpi.GPIO.PUD_DOWN)
    wiringpi.pullUpDnControl(BRIGHTNESS_DEF, wiringpi.GPIO.PUD_DOWN)
    wiringpi.pullUpDnControl(SPEED_ADJ_UP, wiringpi.GPIO.PUD_DOWN)
    wiringpi.pullUpDnControl(SPEED_ADJ_DOWN, wiringpi.GPIO.PUD_DOWN)
    wiringpi.pullUpDnControl(SPEED_DEF, wiringpi.GPIO.PUD_DOWN)

    wiringpi.wiringPiISR(DEFAULT_MODE, wiringpi.GPIO.INT_EDGE_BOTH, default_mode_button_pressed)
    wiringpi.wiringPiISR(MODE_UP, wiringpi.GPIO.INT_EDGE_BOTH, mode_change_up_button_pressed)
    wiringpi.wiringPiISR(MODE_DOWN, wiringpi.GPIO.INT_EDGE_BOTH, mode_change_down_button_pressed)
    wiringpi.wiringPiISR(TURN_OFF, wiringpi.GPIO.INT_EDGE_BOTH, turn_off_lights)
    wiringpi.wiringPiISR(TURN_ON, wiringpi.GPIO.INT_EDGE_BOTH, turn_on_lights)
    wiringpi.wiringPiISR(BRIGHTNESS_UP, wiringpi.GPIO.INT_EDGE_BOTH, brightness_adj_up)
    wiringpi.wiringPiISR(BRIGHTNESS_DOWN, wiringpi.GPIO.INT_EDGE_BOTH, brightness_adj_down)
    wiringpi.wiringPiISR(BRIGHTNESS_DEF, wiringpi.GPIO.INT_EDGE_BOTH, brightness_adj_default)
    wiringpi.wiringPiISR(SPEED_ADJ_DOWN, wiringpi.GPIO.INT_EDGE_BOTH, speed_adj_down)
    wiringpi.wiringPiISR(SPEED_ADJ_UP, wiringpi.GPIO.INT_EDGE_BOTH, speed_adj_up)
    wiringpi.wiringPiISR(SPEED_DEF, wiringpi.GPIO.INT_EDGE_BOTH, speed_adj_default)

    signal.signal(signal.SIGINT, signal_handler)
    signal.pause()

    message = input("Press enter to quit\n\n")
    GPIO.cleanup()
    # print out a message and wait for keyboard input before
    # exiting the program
