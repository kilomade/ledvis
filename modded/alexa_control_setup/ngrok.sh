#!/bin/bash

sudo apt-get update && sudo apt-get upgrade -y
sudo apt-get install python2.7-dev python-dev python-pip 
sudo pip install Flask flask-ask

unzip ngrok-stable-linux-arm64.tgz
cd ngrok-stable-linux-arm64
./ngrok authtoken 1dy7CIZhAacbfK4N2Oya0vDnwCe_6iPb1kVaxP4psrEjxcdc3
./ngrok http 80