from multiprocessing import Process, Array
import pyaudio
import numpy as np
import time
import requests
from config import *
from visualizer import jordyn_vis_list as vis_list
from strips import Strips
from util import FrequencyPrinter, CircularBuffer
from __future__ import absolute_import, division, print_function, \
                                                    unicode_literals
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

def brightness_adj_default(interupt_pin):
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

    brightness_level_index = 5

    runSystemNow()

def brightness_adj_up(interupt_pin):
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

    brightness_level_index += 1

    if brightness_level_index > (brightness_level_index - 1):
        brightness_level_index = 0

    runSystemNow()

def brightness_adj_down(interrupt_pin):
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

    brightness_level_index -= 1

    if brightness_level_index < 0:
        brightness_level_index = (brightness_level_range - 1)

    runSystemNow()

def turn_off_lights(interrupt_pin):
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

def mode_change_up_button_pressed(interrupt_pin):
    global bus
    global mode_index
    bus = None


    mode_index += 1

    if mode_index > (mode_index - 1):
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

def mode_change_down_button_pressed(interrupt_pin):
    global bus
    global mode_index
    bus = None

    if mode_index == 0:
        mode_index -= mode_range - 1
    else:
        mode_index -1
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

def default_mode_button_pressed(interrupt_pin):
    global bus
    global mode_index
    bus = None
    mode_index = 1

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
            print("Pin " + str(num + 1) + " pressed: Default Mode enabled")

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

    strips1 = Strips(
        LED_1_COUNT=LED_2_COUNT,
        LED_1_PIN=LED_2_PIN,
        LED_1_FREQ_HZ=LED_2_FREQ_HZ,
        LED_1_DMA=LED_2_DMA,
        LED_1_INVERT=LED_2_BRIGHTNESS,
        LED_1_BRIGHTNESS=LED_2_INVERT,
        LED_1_CHANNEL=LED_2_CHANNEL
    )

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
    global bus

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
    GPIO.setup(DEFAULT_MODE, GPIO.IN, pull_up_down=GPIO.PUD_OFF)
    GPIO.setup(MODE_UP, GPIO.IN, pull_up_down=GPIO.PUD_OFF)
    GPIO.setup(MODE_DOWN, GPIO.IN, pull_up_down=GPIO.PUD_OFF)
    GPIO.setup(TURN_OFF, GPIO.IN, pull_up_down=GPIO.PUD_OFF)
    GPIO.setup(BRIGHTNESS_UP, GPIO.IN, pull_up_down=GPIO.PUD_OFF)
    GPIO.setup(BRIGHTNESS_DOWN, GPIO.IN, pull_up_down=GPIO.PUD_OFF)
    GPIO.setup(BRIGHTNESS_DEF, GPIO.IN, pull_up_down=GPIO.PUD_OFF)

    # when a falling edge is detected on GPIO 23 the function
    # button_pressed will be run

    GPIO.add_event_detect(DEFAULT_MODE, GPIO.FALLING, callback=default_mode_button_pressed)
    GPIO.add_event_detect(MODE_UP, GPIO.FALLING, callback=mode_change_up_button_pressed)
    GPIO.add_event_detect(MODE_DOWN, GPIO.FALLING, callback=mode_change_down_button_pressed)
    GPIO.add_event_detect(TURN_OFF, GPIO.FALLING, callback=turn_off_lights)
    GPIO.add_event_detect(BRIGHTNESS_UP, GPIO.FALLING, callback=brightness_adj_up)
    GPIO.add_event_detect(BRIGHTNESS_DOWN, GPIO.FALLING, callback=brightness_adj_down)
    GPIO.add_event_detect(BRIGHTNESS_DEF, GPIO.FALLING, callback=brightness_adj_default)
    # print out a message and wait for keyboard input before
    # exiting the program

    input("press enter to exit ")


    