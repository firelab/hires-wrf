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

import json

def usage():
    print("Not enough args!!!\n")
    print("Usage:\n")
    print("hiresWRF path/to/config.json\n")

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

nightly_wrf = config['paths']['nightly_wrf']
logfile = config['paths']['logfile']
dataDir = config['paths']['dataDir']
wpsDir = config['paths']['wpsDir']
runDir = config['paths']['runDir']
outDir = config['paths']['outDir']
ninjaoutDir = config['paths']['ninjaoutDir']

print("logfile: %s" % logfile)
print("nightly_wrf: %s" % nightly_wrf)

#=============================================================================
#        Open a log file
#=============================================================================
time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
log = open(logfile, 'w')
log.write('%s: Starting nightly WRF simulations. \n' % time)

#=============================================================================
#        Run geogrid.exe
#        Only needs to be done once per domain, but make sure namelist.wps
#        is correct.
#        There should be a geo_em* in WPS/ for each domain
#=============================================================================
log.write('#=====================================================\n')
log.write('#              Running geogrid.exe\n')
log.write('#=====================================================\n')

p = subprocess.Popen(["./runGeogrid.py %s" % config_path], cwd = nightly_wrf, shell = True, stdout=subprocess.PIPE)
out, err = p.communicate()

time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
log.write('%s:\n %s \n' % (time, err))
log.write('%s:\n %s \n' % (time, out))

if p.returncode != 0:
    print("runGeogrid: non-zero return code!")
    print(p.returncode)
    time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log.write('%s:\n runGeogrid.py failed with return code %s \n' % (time, p.returncode))
    log.write("!!! Error during runGeogrid !!!")
    log.close()
    sys.exit() #exit with return code 0

#=============================================================================
#        Run ungrib.exe
#=============================================================================
log.write('#=====================================================\n')
log.write('#              Running ungrib.exe \n')
log.write('#=====================================================\n')

p = subprocess.Popen(["./runUngrib.py"], cwd = nightly_wrf, shell = True, stdout=subprocess.PIPE)
out, err = p.communicate()

if p.returncode != 0:
    print("runUngrib.py: non-zero return code!")
    print(p.returncode)
    time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log.write('%s:\n runUngrib.py failed with return code %s \n' % (time, p.returncode))
    log.write("!!! Error during runUngrib !!!")
    log.close()
    sys.exit() #exit with return code 0

#=============================================================================
#        Run metgrid.exe
#=============================================================================
log.write('#=====================================================\n')
log.write('#              Running metgrid.exe \n')
log.write('#=====================================================\n')

p = subprocess.Popen(["export LD_LIBRARY_PATH=/home/natalie/src/wrf/wrf_dependencies/wrf_dependencies/netcdf/lib:$LD_LIBRARY_PATH &&"
    "./metgrid.exe", ">&", "log.metgrid"], cwd = wpsDir, shell = True, stdout=subprocess.PIPE)
out, err = p.communicate()

time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
log.write('%s:\n %s \n' % (time, err))
log.write('%s:\n %s \n' % (time, out))

if p.returncode != 0:
    print("metgrid: non-zero return code!")
    print(p.returncode)
    time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log.write('%s:\n metrid failed with return code %s \n' % (time, p.returncode))
    log.write("!!! Error during metgrid !!!")
    log.close()
    sys.exit() #exit with return code 0

#=============================================================================
#        Run real.exe
#=============================================================================
log.write('#=====================================================\n')
log.write('#              Running real.exe \n')
log.write('#=====================================================\n')

p = subprocess.Popen(["./runReal.py"], cwd = nightly_wrf, shell = True, stdout=subprocess.PIPE)
out, err = p.communicate()

time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
log.write('%s:\n %s \n' % (time, err))
log.write('%s:\n %s \n' % (time, out))

if p.returncode != 0:
    print("runReal: non-zero return code!")
    print(p.returncode)
    time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log.write('%s: runReal.py failed with return code %s \n' % (time, p.returncode))
    log.write("!!! Error during runReal !!!")
    log.close()
    sys.exit() #exit with return code 0

#=============================================================================
#        Run wrf.exe
#=============================================================================
log.write('#=====================================================\n')
log.write('#              Running wrf.exe \n')
log.write('#=====================================================\n')

p = subprocess.Popen(["export LD_LIBRARY_PATH=/home/natalie/src/wrf/wrf_dependencies/wrf_dependencies/netcdf/lib:$LD_LIBRARY_PATH &&"
    "mpirun -np 16 ./wrf.exe"], cwd = runDir, shell = True, stdout=subprocess.PIPE)
out, err = p.communicate()

time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
log.write('%s:\n %s \n' % (time, err))
log.write('%s:\n %s \n' % (time, out))

if p.returncode != 0:
    print("wrf.exe: non-zero return code!")
    print(p.returncode)
    time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log.write('%s: wrf.exe failed with return code %s \n' % (time, p.returncode))
    log.write("!!! Error during wrf.exe !!!")
    log.close()
    sys.exit() #exit with return code 0

#=============================================================================
#        Run WindNinja
#=============================================================================
log.write('#=====================================================\n')
log.write('#              Running WindNinja \n')
log.write('#=====================================================\n')

p = subprocess.Popen(["./runWindNinja.py %s" % config_path], cwd = nightly_wrf, shell = True, stdout=subprocess.PIPE)
out, err = p.communicate()

time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
log.write('%s:\n %s \n' % (time, err))
log.write('%s:\n %s \n' % (time, out))

if p.returncode != 0:
    print("WindNinja: non-zero return code!")
    print(p.returncode)
    time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log.write('%s: WindNinja failed with return code %s \n' % (time, p.returncode))
    log.write("!!! Error during WindNinja !!!")
    log.close()
    sys.exit() #exit with return code 0

#=============================================================================
#        Package output for transfer to server
#=============================================================================
log.write('#=====================================================\n')
log.write('#              Package output files \n')
log.write('#=====================================================\n')
p = subprocess.Popen(["./packageOutput.py %s" % config_path], cwd = nightly_wrf, shell = True, stdout=subprocess.PIPE)
out, err = p.communicate()

#=============================================================================
#        Transfer files to server
#=============================================================================
log.write('#=====================================================\n')
log.write('#              Copying files \n')
log.write('#=====================================================\n')

p = subprocess.Popen(["/home/natalie/hires_wrf/./copyFiles.py %s" % config_path], cwd = nightly_wrf, shell = True, stdout=subprocess.PIPE)
out, err = p.communicate()
print(out)
print(err)

if p.returncode != 0:
    print("copyFiles.py non-zero return code!")
    print(p.returncode)

log.close()

