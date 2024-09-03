#!/usr/bin/env python

import subprocess
import sys
import shutil
import os
from os.path import basename
import re
import zipfile

import datetime
import urllib2

nightly_wrf = '/home/natalie/hires_wrf/'
logfile = nightly_wrf + 'nightlyWRF.log'
WPS = '/home/natalie/src/wrf/WPS/'
RUN = '/home/natalie/src/wrf/WRF/run/'

#=============================================================================
#        Setup environment
#=============================================================================
#p = subprocess.Popen(["/media/natalie/ExtraDrive2/nightly_wrf/./setEnv.sh"], cwd = nightly_wrf, shell = True, stdout=subprocess.PIPE)
#out, err = p.communicate()

#=============================================================================
#        Open a log file
#=============================================================================
time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
log = open(logfile, 'w')
log.write('%s: Starting nightly WRF simulations. \n' % time)

#=============================================================================
#        Clean up from preivous runs
#=============================================================================
log.write('#=====================================================\n')
log.write('#              Cleaning up from previous runs\n')
log.write('#=====================================================\n')

p = subprocess.Popen(["./cleanup.py"], cwd = nightly_wrf, shell = True, stdout=subprocess.PIPE)
out, err = p.communicate()

time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
log.write('%s: %s \n' % (time, err))
log.write('%s: %s \n' % (time, out))

if p.returncode != 0:
    print "cleanup: non-zero return code!"
    print p.returncode
    time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log.write('%s: cleanup.py failed with return code %s \n' % (time, p.returncode))
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
    print "fetchHRRR: non-zero return code!"
    print p.returncode
    time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log.write('%s:\n fetchHRRRR.py failed with return code %s \n' % (time, p.returncode))
    log.write("!!! Error during fetchHRRR !!!")
    log.close()
    sys.exit() #exit with return code 0

#=============================================================================
#        Run geogrid.exe
#        Only needs to be done once per domain, but make sure namelist.wps
#        is correct.
#        There should be a geo_em* in WPS/ for each domain
#=============================================================================
log.write('#=====================================================\n')
log.write('#              Running geogrid.exe\n')
log.write('#=====================================================\n')

p = subprocess.Popen(["./runGeogrid.py"], cwd = nightly_wrf, shell = True, stdout=subprocess.PIPE)
out, err = p.communicate()

time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
log.write('%s:\n %s \n' % (time, err))
log.write('%s:\n %s \n' % (time, out))

if p.returncode != 0:
    print "runGeogrid: non-zero return code!"
    print p.returncode
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
    print "runUngrib.py: non-zero return code!"
    print p.returncode
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

p = subprocess.Popen(["./metgrid.exe", ">&", "log.metgrid"], cwd = WPS, shell = True, stdout=subprocess.PIPE)
out, err = p.communicate()

time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
log.write('%s:\n %s \n' % (time, err))
log.write('%s:\n %s \n' % (time, out))

if p.returncode != 0:
    print "metgrid: non-zero return code!"
    print p.returncode
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
    print "runReal: non-zero return code!"
    print p.returncode
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

p = subprocess.Popen(["mpirun -np 16 ./wrf.exe"], cwd = RUN, shell = True, stdout=subprocess.PIPE)
out, err = p.communicate()

time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
log.write('%s:\n %s \n' % (time, err))
log.write('%s:\n %s \n' % (time, out))

if p.returncode != 0:
    print "wrf.exe: non-zero return code!"
    print p.returncode
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

p = subprocess.Popen(["./runWindNinja.py"], cwd = nightly_wrf, shell = True, stdout=subprocess.PIPE)
out, err = p.communicate()

time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
log.write('%s:\n %s \n' % (time, err))
log.write('%s:\n %s \n' % (time, out))

if p.returncode != 0:
    print "WindNinja: non-zero return code!"
    print p.returncode
    time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log.write('%s: WindNinja failed with return code %s \n' % (time, p.returncode))
    log.write("!!! Error during WindNinja !!!")
    log.close()
    sys.exit() #exit with return code 0

#=============================================================================
#        Copy files for display/download on server
#=============================================================================
log.write('#=====================================================\n')
log.write('#              Copying files \n')
log.write('#=====================================================\n')
p = subprocess.Popen(["./packageOutput.py"], cwd = nightly_wrf, shell = True, stdout=subprocess.PIPE)
out, err = p.communicate()

#copy the WRF-SURFACE*.kml, WRF-SURFACE*.bmp, timestamp file, and the WindNinja output files
p = subprocess.Popen(["/home/natalie/hires_wrf/./copyFiles.py"], cwd = nightly_wrf, shell = True, stdout=subprocess.PIPE)
out, err = p.communicate()
print out
print err

if p.returncode != 0:
    print "copyFiles.py: non-zero return code!"
    print p.returncode

log.close()
