#!/bin/bash

sudo apt-get install portaudio19-dev python-pyaudio python3-pyaudio
pip install adafruit-ads1x15	# install the ADS1015 i2c library
pip3 install Flask				# get Flask (best to use python3)
sudo apt install screen 		# get screen

echo "Intall rpi_ws281x library"

cd ~
git clone https://github.com/jgarff/rpi_ws281x.git
sudo apt install scons swig
cd rpi_ws281x
scons
cd python
sudo -H python setup.py build
sudo -H python setup.py install

