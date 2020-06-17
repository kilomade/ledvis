from __future__ import absolute_import, division, print_function, unicode_literals

from multiprocessing import Process, Array
import pyaudio
import numpy as np
import time
import requests
from config import *
from visualizer import vis_list
from strips import Strips
from util import FrequencyPrinter, CircularBuffer

import time
import RPi.GPIO as GPIO

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

bus = None

#Mode Changes
modes = vis_list
mode_range = len(modes)
mode_index = 0

#Light levels
light_brightness_levels = [
    50,
    75,
    100,
    125,
    150,
    175,
    200,
    225,
    255
]

brightness_level_index = 4
brightness_level_range = len(light_brightness_levels)

#Speed Changes
speed_levels = [
    0.001,
    0.0025,
    0.005,
    0.05,
    0.5,
    1,
    3,
    5
]

speed_level_index = 2
speed_level_range = len(speed_levels)

#TODO finish this method for changing modes, brightness, and speed
def messageReceived(identifier):
    assignments = {
        101: changeMode(identifier=13),
        102: changeMode(identifier=0),
        103: brightness_adj(trigger=1),
        104: brightness_adj(trigger=0),
        105: brightness_adj(trigger=2),
        106: speed_adj(trigger=1),
        107: speed_adj(trigger=0),
        108: speed_adj(trigger=2),
        201: changeMode(identifier=1),
        202: changeMode(identifier=2),
        203: changeMode(identifier=3),
        204: changeMode(identifier=4),
        205: changeMode(identifier=5),
        206: changeMode(identifier=6),
        207: changeMode(identifier=7),
        208: changeMode(identifier=8),
        209: changeMode(identifier=9),
        210: changeMode(identifier=10),
        211: changeMode(identifier=11),
        212: changeMode(identifier=12)
    }

    assignments[identifier]

def speed_adj(trigger):
    global light_brightness_levels
    global speed_level_index
    global speed_levels
    global bus
    global LED_WRITE_DELAY

    bus = None

    if trigger == 0:
        #Default mode
        speed_level_index = 2
    elif trigger == 1:
        #Increase Speed
        speed_level_index += 1
    elif trigger == 2:
        #Decrease speed
        speed_level_index -= 1

    LED_WRITE_DELAY = speed_levels[speed_level_index]

    """
    this function will be called when GPIO 23 falls low
    """
    # read the interrupt capture for port 0 and store it in variable intval
    intval = bus.read_interrupt_capture(0)

    # compare the value of intval with the IO Pi port 0
    # using read_port().  wait until the port changes which will indicate
    # the button has been released.
    # without this while loop the function will keep repeating.

    while (intval == bus.read_port(0)):
        time.sleep(0.2)

    # loop through each bit in the intval variable and check if the bit is 1
    # which will indicate a button has been pressed
    for num in range(0, 8):
        if (intval & (1 << num)):
            print("Pin " + str(num + 1) + " pressed: Mode Changed to " + str(modes[mode_index]))

    runSystemNow()

def brightness_adj(trigger, levelIndicator=None):
    global light_brightness_levels
    global brightness_level_index
    global bus
    bus = None

    """
    this function will be called when GPIO 23 falls low
    """
    # read the interrupt capture for port 0 and store it in variable intval
    intval = bus.read_interrupt_capture(0)

    # compare the value of intval with the IO Pi port 0
    # using read_port().  wait until the port changes which will indicate
    # the button has been released.
    # without this while loop the function will keep repeating.

    while (intval == bus.read_port(0)):
        time.sleep(0.2)

    # loop through each bit in the intval variable and check if the bit is 1
    # which will indicate a button has been pressed
    for num in range(0, 8):
        if (intval & (1 << num)):
            print("Pin " + str(num + 1) + " pressed: Mode Changed to " + str(modes[mode_index]))


    if levelIndicator is not None:
        if levelIndicator == 20:
            config.LED_1_BRIGHTNESS = 52
        elif levelIndicator == 40:
            config.LED_1_BRIGHTNESS = 102
        elif levelIndicator == 60:
            config.LED_1_BRIGHTNESS = 153
        elif levelIndicator == 80:
            config.LED_1_BRIGHTNESS = 204
        elif levelIndicator == 100:
            config.LED_1_BRIGHTNESS = 255
    else:
        if trigger == 0:
            brightness_level_index = 5

            config.LED_1_BRIGHTNESS = light_brightness_levels[brightness_level_index]
        elif trigger == 1:
            brightness_level_index += 1

            if brightness_level_index > (brightness_level_index - 1):
                brightness_level_index = 0

            config.LED_1_BRIGHTNESS = light_brightness_levels[brightness_level_index]
        elif trigger == 2:
            brightness_level_index -= 1

            if brightness_level_index < 0:
                brightness_level_index = (brightness_level_range - 1)

            config.LED_1_BRIGHTNESS = light_brightness_levels[brightness_level_index]

    runSystemNow()

def turn_off_lights():
    global bus
    global mode_index
    bus = None
    mode_index = 0
    """
    this function will be called when GPIO 23 falls low
    """
    # read the interrupt capture for port 0 and store it in variable intval
    intval = bus.read_interrupt_capture(0)

    # compare the value of intval with the IO Pi port 0
    # using read_port().  wait until the port changes which will indicate
    # the button has been released.
    # without this while loop the function will keep repeating.

    while (intval == bus.read_port(0)):
        time.sleep(0.2)

    # loop through each bit in the intval variable and check if the bit is 1
    # which will indicate a button has been pressed
    for num in range(0, 8):
        if (intval & (1 << num)):
            print("Pin " + str(num + 1) + " pressed: Mode Changed to " + str(modes[mode_index]))

    runSystemNow()

def turn_on_lights():
    global bus
    global mode_index
    bus = None
    mode_index = 0
    """
    this function will be called when GPIO 23 falls low
    """
    # read the interrupt capture for port 0 and store it in variable intval
    intval = bus.read_interrupt_capture(0)

    # compare the value of intval with the IO Pi port 0
    # using read_port().  wait until the port changes which will indicate
    # the button has been released.
    # without this while loop the function will keep repeating.

    while (intval == bus.read_port(0)):
        time.sleep(0.2)

    # loop through each bit in the intval variable and check if the bit is 1
    # which will indicate a button has been pressed
    for num in range(0, 8):
        if (intval & (1 << num)):
            print("Pin " + str(num + 1) + " pressed: Mode Changed to " + str(modes[mode_index]))

    runSystemNow()

def changeMode(identifier):
    global bus
    global mode_index
    bus = None

    mode_index = identifier

    runSystemNow()


def runSystemNow():
    sample_array = Array('i', np.zeros(SAMPLE_ARRAY_SIZE + 1, dtype=int))
    settings_array = Array('i', np.zeros(1, dtype=int))

    sampler_process = Process(target=sampler, name='Sampler', args=(sample_array,))
    visualizer_process = Process(target=visualizer, name='Visualizer', args=(sample_array, settings_array))
    settings_process = Process(target=settings_getter, name='Settings Getter', args=(settings_array,))

    processes = [sampler_process, visualizer_process, settings_process]

    for p in processes: p.start()
    for p in processes: print("Started {} on PID {}".format(p.name, p.pid))
    for p in processes: p.join()


def sampler(sample_array):
    '''
    Sample the ADC as in continous mode and write into the shared array as a circular buffer.
    The index that has been most recently written is stored in the last slot in the array
    '''

    audio = pyaudio.PyAudio() # create pyaudio instantiation

    # create pyaudio stream
    stream = audio.open(format=FORMAT, rate=SAMPLING_FREQ, channels=NUM_CHANNELS, \
                        input_device_index=DEVICE_INDEX, input=True, \
                        frames_per_buffer=CHUNK_SIZE)

    fp = FrequencyPrinter('Sampler')
    while True:
        if PRINT_LOOP_FREQUENCY: fp.tick()

        try:
            data = stream.read(CHUNK_SIZE)
        except IOError:
            print('Stream overflow!')
            stream.close()
            stream = audio.open(format=FORMAT, rate=SAMPLING_FREQ, channels=NUM_CHANNELS, \
                        input_device_index=DEVICE_INDEX, input=True, \
                        frames_per_buffer=CHUNK_SIZE)
        int_data = np.fromstring(data, dtype="int16")
        # print stream.get_read_available()

        # attempts a non-blocking write to the sample array
        if sample_array.acquire(False):
            sample_start = sample_array[-1]
            sample_end = sample_start + CHUNK_SIZE

            if sample_end < SAMPLE_ARRAY_SIZE - 1:
                sample_array[sample_start:sample_end] = int_data # write the newest sample to the array
                sample_array[-1] = sample_end # store the most recent index last in the array
            # else:
            #     print 'dropped'

            sample_array.release()

    # here I was saving some sample data for testing offline
    # a = np.array(samples)
    # print 'Saving', a.shape, 'samples'
    # np.save("sample_30s_3.txt", np.array(samples), allow_pickle=True)


def visualizer(sample_array, settings_array):
    global mode_index
    '''
    Create an array of colors to be displayed on the LED strips given an array of audio samples
    '''

    # strips = Strips(
    #     LED_1_COUNT=None,
    #     LED_1_PIN=None,
    #     LED_1_FREQ_HZ=None,
    #     LED_1_DMA=None,
    #     LED_1_INVERT=None,
    #     LED_1_BRIGHTNESS=None,
    #     LED_1_CHANNEL=None
    # )
    strips = Strips(
        LED_1_COUNT=LED_1_COUNT,
        LED_1_PIN=LED_1_PIN,
        LED_1_FREQ_HZ=LED_1_FREQ_HZ,
        LED_1_DMA=LED_1_DMA,
        LED_1_INVERT=LED_1_BRIGHTNESS,
        LED_1_BRIGHTNESS=LED_1_INVERT,
        LED_1_CHANNEL=LED_1_CHANNEL
    )

    # strips1 = Strips(
    #     LED_1_COUNT=LED_2_COUNT,
    #     LED_1_PIN=LED_2_PIN,
    #     LED_1_FREQ_HZ=LED_2_FREQ_HZ,
    #     LED_1_DMA=LED_2_DMA,
    #     LED_1_INVERT=LED_2_BRIGHTNESS,
    #     LED_1_BRIGHTNESS=LED_2_INVERT,
    #     LED_1_CHANNEL=LED_2_CHANNEL
    # )

    vis_index = -1
    new_vis_index = mode_index

    fp = FrequencyPrinter('Visualizer')
    while True:
        if PRINT_LOOP_FREQUENCY: fp.tick()

        # get the current selected mode
        if settings_array.acquire():
            new_vis_index = settings_array[0]
            settings_array.release()

        # if the selected mode has changed, instantiate the new visualizer
        if vis_index != new_vis_index:
            vis_index = new_vis_index
            vis = vis_list[vis_index]()
            circ_buffer = CircularBuffer(vis.required_samples)
            print('Mode changed to {}'.format(vis.name))

        # get the newest sample array
        sample_array.acquire()
        a = np.array(sample_array[:sample_array[-1]])
        sample_array[-1] = 0 # indicate that you have read the sample
        sample_array.release()

        # add the array to the buffer
        circ_buffer.push(a)

        # run the visualizer on the contents of the buffer
        color_array = vis.visualize(circ_buffer.get())

        # send the color array to the strips
        strips.write(color_array)
        strips1.write(color_array)

def settings_getter(settings_array):
    '''
    Make get requests to the server to get the most recent user input
    '''
    fp = FrequencyPrinter('Settings Getter')
    while True:
        if PRINT_LOOP_FREQUENCY: fp.tick()

        # do a get request to the server
        url = 'http://ledvis.local:5000/get_settings'

        try:
            response = requests.get(url)
        except requests.ConnectionError:
            print('Request failed.')
            continue

        if response.ok:
            data = response.json()
            vis_index = int(data['vis_index'])
            settings_array.acquire()
            settings_array[0] = vis_index
            settings_array.release()
        else:
            print('Status Code {}'.format(response.status_code))

        time.sleep(0.1)


if __name__ == '__main__':

    # Create an instance of the IOPi class called bus and
    # set the I2C address to be 0x20 or Bus 1.

    bus = IOPi(0x20)

    # Set port 0 on the bus to be inputs with internal pull-ups enabled.

    bus.set_port_pullups(0, 0xFF)
    bus.set_port_direction(0, 0xFF)

    # Inverting the port will allow a button connected to ground to
    # register as 1 or on.

    bus.invert_port(0, 0xFF)

    # Set the interrupt polarity to be active low so Int A and IntB go low
    # when an interrupt is triggered and mirroring disabled, so
    # Int A is mapped to port 0 and Int B is mapped to port 1

    bus.set_interrupt_polarity(0)
    bus.mirror_interrupts(0)

    # Set the interrupts default value to 0 so it will trigger when any of
    # the pins on the port 0 change to 1

    bus.set_interrupt_defaults(0, 0x00)

    # Set the interrupt type to be 0xFF so an interrupt is
    # fired when the pin matches the default value

    bus.set_interrupt_type(0, 0xFF)

    # Enable interrupts for all pins on port 0

    bus.set_interrupt_on_port(0, 0xFF)

    # reset the interrups on the IO Pi bus

    bus.reset_interrupts()

    # set the Raspberry Pi GPIO mode to be BCM

    GPIO.setmode(GPIO.BCM)

    # Set up GPIO 23 as an input. The pull-up resistor is disabled as the
    # level shifter will act as a pull-up.
    GPIO.setup(MODE_DOWN, GPIO.IN, pull_up_down=GPIO.PUD_OFF)

    # print out a message and wait for keyboard input before
    # exiting the program

    input("press enter to exit ")
