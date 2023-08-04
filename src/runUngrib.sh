#!/bin/bash

echo "Running ungrib..."

source /home/natalie/.bashrc

export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/opt/jasper/lib/ && /home/natalie/src/wrf/WPS/./ungrib.exe >ungrib.log 2>&1
