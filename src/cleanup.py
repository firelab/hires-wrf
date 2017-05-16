#!/usr/bin/env python

import os
import re

dataDir = '/home/nwagenbrenner/nightly_wrf/data'
wpsDir = '/home/nwagenbrenner/src/WRF/WPS'

#=============================================================================
#        Clean up HRRR
#=============================================================================
#for f in os.listdir(dataDir):
#    f_path = os.path.join(dataDir, f)
#    try:
#        if os.path.isfile(f_path):
#            os.unlink(f_path)
#    except Exception as e:
#        print(e)
#
#print 'HRRR cleanup complete!'

#=============================================================================
#        Clean up WPS
#=============================================================================
#pattern = "FILE:"
#for f in os.listdir(wpsDir):
#    if re.search(pattern, f): 
#        f_path = os.path.join(wpsDir, f)
#        try:
#            if os.path.isfile(f_path):
#                os.unlink(f_path)
#        except Exception as e:
#            print(e)
#
#pattern = "met_em."
#for f in os.listdir(wpsDir):
#    if re.search(pattern, f): 
#        f_path = os.path.join(wpsDir, f)
#        try:
#            if os.path.isfile(f_path):
#                os.unlink(f_path)
#        except Exception as e:
#            print(e)
#
#pattern = "GRIBFILE."
#for f in os.listdir(wpsDir):
#    if re.search(pattern, f): 
#        f_path = os.path.join(wpsDir, f)
#        try:
#            if os.path.isfile(f_path):
#                os.unlink(f_path)
#        except Exception as e:
#            print(e)
#
#print 'WPS cleanup complete!'
#
#print 'Cleanup complete!'
