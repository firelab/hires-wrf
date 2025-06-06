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

RUN = config['paths']['RUN']
outDir = config['paths']['outDir']
ninjaoutDir = config['paths']['ninjaoutDir']

print("Running: WindNinja_cli %swrf_initialization.cfg" % outDir)

logfile = outDir + 'runWindNinja.log'
log = open(logfile, 'w')
log.write('Starting WindNinja simulations. \n')

start_year = datetime.date.today().year
start_month = datetime.date.today().month
start_day = datetime.date.today().day

#copy wrfout file to output directory
log.write('Copying wrfout file. \n')
wrfoutSrc = RUN + ('wrfout_d01_%s-%02d-%02d_18:00:00' % (start_year, start_month, start_day))
wrfoutDst = outDir + 'wrfout.nc'  
shutil.copyfile(wrfoutSrc, wrfoutDst) 
log.write('Done copying wrfout file. \n')

#source /home/natalie/.bashrc
log.write('Starting WindNinja. \n')
p = subprocess.Popen(["export WINDNINJA_DATA=/home/natalie/src/windninja/windninja/data && /usr/local/bin/WindNinja_cli %swrf_initialization.cfg" % outDir], cwd = outDir, shell = True, stdout=subprocess.PIPE)
out, err = p.communicate()
log.write('WindNinja out: %s. \n' % out)
log.write('WindNinja err: %s. \n' % err)
log.write('Done running WindNinja. \n')

if p.returncode != 0:
    print("WindNinja: non-zero return code!")
    print(p.returncode)

log.close()
