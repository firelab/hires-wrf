#!/usr/bin/env python3

import subprocess
import sys
import shutil
import os
from os.path import basename
import re
import zipfile

import datetime
import urllib.request

nightly_wrf = '/home/natalie/hires_wrf/'
logfile = nightly_wrf + 'nightlyWRF.log'
d01_config = nightly_wrf + 'output/d01/config.json'
d02_config = nightly_wrf + 'output/d02/config.json'
d03_config = nightly_wrf + 'output/d03/config.json'

#=============================================================================
#        Open a log file
#=============================================================================
time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
log = open(logfile, 'w')
log.write('%s: Starting nightly WRF simulations. \n' % time)

#=============================================================================
#       Clean up from previous runs 
#=============================================================================
log.write('#=====================================================\n')
log.write('#              Cleaning Up\n')
log.write('#=====================================================\n')

p = subprocess.Popen(["./cleanup.py"], cwd = nightly_wrf, shell = True, stdout=subprocess.PIPE)
out, err = p.communicate()

time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
log.write('%s:\n %s \n' % (time, err))
log.write('%s:\n %s \n' % (time, out))

if p.returncode != 0:
    print("cleanup: non-zero return code!")
    print(p.returncode)
    time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log.write('%s:\n cleanup.py failed with return code %s \n' % (time, p.returncode))
    log.write("!!! Error during cleanup !!!")
    log.close()
    sys.exit() #exit with return code 0

#=============================================================================
#        Download HRRR
#=============================================================================
log.write('#=====================================================\n')
log.write('#              Downloading HRRR \n')
log.write('#=====================================================\n')

p = subprocess.Popen(["./fetchHRRR.py"], cwd = nightly_wrf, shell = True, stdout=subprocess.PIPE)
out, err = p.communicate()

time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
log.write('%s:\n %s \n' % (time, err))
log.write('%s:\n %s \n' % (time, out))

if p.returncode != 0:
    print("fetchHRRR: non-zero return code!")
    print(p.returncode)
    time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log.write('%s:\n fetchHRRRR.py failed with return code %s \n' % (time, p.returncode))
    log.write("!!! Error during fetchHRRR !!!")
    log.close()
    sys.exit() #exit with return code 0

#=============================================================================
#       Run first domain 
#=============================================================================
log.write('#=====================================================\n')
log.write('#              Running Domain d01\n')
log.write('#=====================================================\n')

p = subprocess.Popen(["./hiresWRF.py %s" % d01_config], cwd = nightly_wrf, shell = True, stdout=subprocess.PIPE)
out, err = p.communicate()

time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
log.write('%s:\n %s \n' % (time, err))
log.write('%s:\n %s \n' % (time, out))

if p.returncode != 0:
    print("hiresWRF: non-zero return code!")
    print(p.returncode)
    time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log.write('%s:\n hiresWRF.py failed with return code %s \n' % (time, p.returncode))
    log.write("!!! Error during hiresWRF !!!")
    log.close()
    sys.exit() #exit with return code 0

#=============================================================================
#       Run second domain 
#=============================================================================
log.write('#=====================================================\n')
log.write('#              Running Domain d02\n')
log.write('#=====================================================\n')

p = subprocess.Popen(["./hiresWRF.py %s" % d02_config], cwd = nightly_wrf, shell = True, stdout=subprocess.PIPE)
out, err = p.communicate()

time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
log.write('%s:\n %s \n' % (time, err))
log.write('%s:\n %s \n' % (time, out))

if p.returncode != 0:
    print("hiresWRF: non-zero return code!")
    print(p.returncode)
    time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log.write('%s:\n hiresWRF.py failed with return code %s \n' % (time, p.returncode))
    log.write("!!! Error during hiresWRF !!!")
    log.close()
    sys.exit() #exit with return code 0

#=============================================================================
#       Run third domain 
#=============================================================================
log.write('#=====================================================\n')
log.write('#              Running Domain d03\n')
log.write('#=====================================================\n')

p = subprocess.Popen(["./hiresWRF.py %s" % d03_config], cwd = nightly_wrf, shell = True, stdout=subprocess.PIPE)
out, err = p.communicate()

time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
log.write('%s:\n %s \n' % (time, err))
log.write('%s:\n %s \n' % (time, out))

if p.returncode != 0:
    print("hiresWRF: non-zero return code!")
    print(p.returncode)
    time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log.write('%s:\n hiresWRF.py failed with return code %s \n' % (time, p.returncode))
    log.write("!!! Error during hiresWRF !!!")
    log.close()
    sys.exit() #exit with return code 0

log.close()
