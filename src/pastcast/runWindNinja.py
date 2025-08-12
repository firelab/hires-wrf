#!/usr/bin/env python3

import subprocess
import shutil
import os
import re
import datetime
import sys
import json

def usage():
    print("Not enough args!!!\n")
    print("Usage:\n")
    print("runWindNinja path/to/config.json\n")

if len(sys.argv) != 2:
    usage()
    sys.exit()

config_path = sys.argv[1]
print("The input config_path is: %s" % config_path)

#=============================================================================
#        Setup paths for current domain
#=============================================================================
with open(config_path, 'r') as f:
    config = json.load(f)

runDir = config['paths']['runDir']
outDir = config['paths']['outDir']
ninjaoutDir = config['paths']['ninjaoutDir']
nightlyWRF = config['paths']['nightly_wrf']
lat = config['location']['lat']
lon = config['location']['lon']
start_year = config['datetime']['startYear']
start_month = config['datetime']['startMonth']
start_day = config['datetime']['startDay']
start_hour = config['datetime']['startHour']

print("Running: WindNinja_cli %swrf_initialization.cfg" % outDir)

logfile = outDir + 'runWindNinja.log'
log = open(logfile, 'w')
log.write('Starting WindNinja simulations. \n')

#copy wrfout file to output directory
log.write('Copying wrfout file. \n')
wrfoutSrc = runDir + ('wrfout_d01_%s-%s-%s_%s:00:00' % (start_year, start_month, start_day, start_hour))
wrfoutDst = outDir + 'wrfout.nc'  
shutil.copyfile(wrfoutSrc, wrfoutDst) 
log.write('Done copying wrfout file. \n')

#source /home/natalie/.bashrc
log.write('Starting WindNinja. \n')

print( "%swrf_initialization.cfg "
        "--fetch_elevation %sdem.tif "
        "--x_center %s "
        "--y_center %s "
        "--forecast_filename %swrfout.nc "
        "--output_path %s" % (nightlyWRF, outDir, lon, lat, outDir, ninjaoutDir)) 

#export HDF5_DISABLE_VERSION_CHECK is to ignore error that is arising due to conflicting HDF5 libs
#could try setting LD_LIBRARY_PATH
p = subprocess.Popen(["export WINDNINJA_DATA=/home/natalie/src/windninja/windninja/data && export HDF5_DISABLE_VERSION_CHECK=1 && /usr/local/bin/WindNinja_cli "
        "%swrf_initialization.cfg "
        "--fetch_elevation %sdem.tif "
        "--x_center %s "
        "--y_center %s "
        "--forecast_filename %swrfout.nc "
        "--output_path %s" % (nightlyWRF, outDir, lon, lat, outDir, ninjaoutDir)], 
        cwd = outDir, 
        shell = True, 
        stdout=subprocess.PIPE)

out, err = p.communicate()
log.write('WindNinja out: %s. \n' % out)
log.write('WindNinja err: %s. \n' % err)
log.write('Done running WindNinja. \n')

if p.returncode != 0:
    print("WindNinja: non-zero return code!")
    print(p.returncode)

log.close()
