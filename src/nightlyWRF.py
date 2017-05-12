#!/usr/bin/env python

import subprocess
import sys

import datetime
import urllib2

nightly_wrf = '/home/nwagenbrenner/nightly_wrf/'
logfile = nightly_wrf + 'output/nightlyWRF.log'
WPS = '/home/nwagenbrenner/src/WRF/WPS/'

#=============================================================================
#        Open a log file
#=============================================================================
time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
log = open(logfile, 'w')
log.write('%s: Starting nightly WRF simulations. \n' % time)

#=============================================================================
#        Download HRRR
#=============================================================================
log.write('#=====================================================\n')
log.write('#              Downloading HRRR \n')
log.write('#=====================================================\n')

p = subprocess.Popen(["./fetchHRRR.py"], cwd = nightly_wrf, shell = True, stdout=subprocess.PIPE)
out, err = p.communicate()

time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
log.write('%s: %s \n' % (time, err))
log.write('%s: %s \n' % (time, out))

if p.returncode != 0:
    print "fetchHRRR: non-zero return code!"
    print p.returncode
    time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log.write('%s: fetchHRRRR.py failed with return code %s \n' % (time, p.returncode))
    log.write("!!! Error during fetchHRRR !!!")
    log.close()
    sys.exit() #exit with return code 0

#=============================================================================
#        Run geogrid.exe
#=============================================================================
log.write('#=====================================================\n')
log.write('#              Running geogrid.exe\n')
log.write('#=====================================================\n')

p = subprocess.Popen(["./runGeogrid.py"], cwd = nightly_wrf, shell = True, stdout=subprocess.PIPE)
out, err = p.communicate()

if p.returncode != 0:
    print "runGeogrid: non-zero return code!"
    print p.returncode
    time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log.write('%s: runGeogrid.py failed with return code %s \n' % (time, p.returncode))
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
    log.write('%s: runUngrib.py failed with return code %s \n' % (time, p.returncode))
    log.write("!!! Error during runUngrig !!!")
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

if p.returncode != 0:
    print "runMetgrid: non-zero return code!"
    print p.returncode
    time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log.write('%s: runMetgrid.py failed with return code %s \n' % (time, p.returncode))
    log.write("!!! Error during runMetgrid !!!")
    log.close()
    sys.exit() #exit with return code 0

#=============================================================================
#        Clean up
#=============================================================================
log.close()
