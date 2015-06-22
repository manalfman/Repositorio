#!/bin/bash
# -*- ENCODING: UTF-8 -*-
LD_LIBRARY_PATH=../usr/local/lib mjpg_streamer -i "input_raspicam.so -x 640 -y 480 -fps 20 -ex night" -o "output_http.so -w ./www" 
