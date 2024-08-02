#!/usr/bin/env python

import os
import re

dataDir = '/home/natalie/hires_wrf/data'
wpsDir = '/home/natalie/src/wrf/WPS'
runDir = '/home/natalie/src/wrf/WRF/run/'
nightly_wrf = '/home/natalie/hires_wrf/'
outDir = nightly_wrf + "output/"
ninjaoutDir = outDir + "ninjaout/"

#=============================================================================
#        Clean up WindNinja output
#=============================================================================
for f in os.listdir(ninjaoutDir):
    f_path = os.path.join(ninjaoutDir, f)
    try:
        if os.path.isfile(f_path):
            os.unlink(f_path)
    except Exception as e:
        print(e)

print 'WindNinja cleanup complete!'

#=============================================================================
#        Clean up HRRR
#=============================================================================
for f in os.listdir(dataDir):
    f_path = os.path.join(dataDir, f)
    try:
        if os.path.isfile(f_path):
            os.unlink(f_path)
    except Exception as e:
        print(e)

print 'HRRR cleanup complete!'

#=============================================================================
#        Clean up WPS
#=============================================================================
pattern = "FILE:"
for f in os.listdir(wpsDir):
    if re.search(pattern, f): 
        f_path = os.path.join(wpsDir, f)
        try:
            if os.path.isfile(f_path):
                os.unlink(f_path)
        except Exception as e:
            print(e)

pattern = "met_em."
for f in os.listdir(wpsDir):
    if re.search(pattern, f): 
        f_path = os.path.join(wpsDir, f)
        try:
            if os.path.isfile(f_path):
                os.unlink(f_path)
        except Exception as e:
            print(e)

pattern = "GRIBFILE."
for f in os.listdir(wpsDir):
    if re.search(pattern, f): 
        f_path = os.path.join(wpsDir, f)
        try:
            os.unlink(f_path)
        except Exception as e:
            print(e)

print 'WPS cleanup complete!'

#=============================================================================
#        Clean up run directory
#=============================================================================
pattern = "met_em."
for f in os.listdir(runDir):
    if re.search(pattern, f): 
        f_path = os.path.join(runDir, f)
        try:
            os.unlink(f_path)
        except Exception as e:
            print(e)

pattern = "wrfout_"
for f in os.listdir(runDir):
    if re.search(pattern, f): 
        f_path = os.path.join(runDir, f)
        try:
            os.unlink(f_path)
        except Exception as e:
            print(e)

print 'run cleanup complete!'

print 'Cleanup complete!'
