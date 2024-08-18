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

import json

def usage():
    print("Not enough args!!!\n")
    print("Usage:\n")
    print("packageOutput path/to/config.json\n")

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
outDir = config['paths']['outDir']
ninjaoutDir = config['paths']['ninjaoutDir']

#nightly_wrf = '/home/natalie/hires_wrf/'
#outDir = nightly_wrf + "output/"
#ninjaoutDir = outDir + "ninjaout/"

#=============================================================================
#        Copy files for display on server
#=============================================================================

#####-------- stip out kml and other info for the server --------------#############
#rename from .kmz to .zip
pattern = "WRF-SURFACE-"
for f in os.listdir(ninjaoutDir):
    if re.search(pattern, f): 
        f_path = os.path.join(ninjaoutDir, f)
        try:
            if os.path.isfile(f_path):
                base = os.path.splitext(f_path)[0]
                os.rename(f_path, base + '.zip')
        except Exception as e:
            print(e)

#unzip the kmz files 
pattern = ".zip"
for f in os.listdir(ninjaoutDir):
    if re.search(pattern, f): 
        f_path = os.path.join(ninjaoutDir, f)
        try:
            if os.path.isfile(f_path):
                with zipfile.ZipFile(f_path, 'r') as zip_ref:
                    zip_ref.extractall(ninjaoutDir)
        except Exception as e:
            print(e)

#rename the files to wrf_1200.kml and 1200.bmp, for example
pattern = ".kml"
for f in os.listdir(ninjaoutDir):
    if re.search(pattern, f): 
        f_path = os.path.join(ninjaoutDir, f)
        try:
            if os.path.isfile(f_path):
                os.rename(f_path, ninjaoutDir + 'wrf_' + f_path[-8:])
        except Exception as e:
            print(e)

pattern = ".bmp"
for f in os.listdir(ninjaoutDir):
    if re.search(pattern, f): 
        if re.search("date_time", f):
            continue
        f_path = os.path.join(ninjaoutDir, f)
        try:
            if os.path.isfile(f_path):
                os.rename(f_path, ninjaoutDir + f_path[-8:])
        except Exception as e:
            print(e)

#update the timestamp file for display on the webpage
today = datetime.datetime.now().strftime('%Y-%m-%d')
wxLogFile = ninjaoutDir + 'wxLog.txt'
wxLog = open(wxLogFile, 'w')
wxLog.write('High-Resolution WRF\n')
wxLog.write('All timesteps are in local time.\n')
wxLog.write('Simulation valid for: %s.\n' % today)
wxLog.close()

#rename back to .kmz 
pattern = ".zip"
for f in os.listdir(ninjaoutDir):
    if re.search(pattern, f): 
        f_path = os.path.join(ninjaoutDir, f)
        try:
            if os.path.isfile(f_path):
                base = os.path.splitext(f_path)[0]
                os.rename(f_path, base + '.kmz')
        except Exception as e:
            print(e)


#####-------- Zip things up for easier transfer --------------#############
#zip the kmz files into an archive to copy to ninjastorm
pattern = "WRF-SURFACE.*.kmz"
with zipfile.ZipFile((os.path.join(ninjaoutDir, "wrf.zip")), 'w') as zip_ref:
    for f in os.listdir(ninjaoutDir):
        if re.search(pattern, f): 
            f_path = os.path.join(ninjaoutDir, f)
            try:
                if os.path.isfile(f_path):
                    zip_ref.write(f_path, basename(f_path))
            except Exception as e:
                print(e)
zip_ref.close()

#pattern = ".kmz"
#with zipfile.ZipFile((os.path.join(ninjaoutDir, "kmz.zip")), 'w') as zip_ref:
#    for f in os.listdir(ninjaoutDir):
#        if re.search(pattern, f): 
#            f_path = os.path.join(ninjaoutDir, f)
#            try:
#                if os.path.isfile(f_path):
#                    zip_ref.write(f_path, basename(f_path))
#            except Exception as e:
#                print(e)
#zip_ref.close()

#zip the raster files into an archive to copy to breezy
#pattern = ".asc"
#with zipfile.ZipFile((os.path.join(ninjaoutDir, "raster.zip")), 'w') as zip_ref:
#    for f in os.listdir(ninjaoutDir):
#        if re.search(pattern, f): 
#            f_path = os.path.join(ninjaoutDir, f)
#            try:
#                if os.path.isfile(f_path):
#                    zip_ref.write(f_path, basename(f_path))
#            except Exception as e:
#                print(e)
#    pattern = ".prj"
#    for f in os.listdir(ninjaoutDir):
#        if re.search(pattern, f): 
#            f_path = os.path.join(ninjaoutDir, f)
#            try:
#                if os.path.isfile(f_path):
#                    zip_ref.write(f_path, basename(f_path))
#            except Exception as e:
#                print(e)
#zip_ref.close()
#
##zip the shapefile files into an archive to copy to breezy
#pattern = ".shp"
#with zipfile.ZipFile((os.path.join(ninjaoutDir, "shapefile.zip")), 'w') as zip_ref:
#    for f in os.listdir(ninjaoutDir):
#        if re.search(pattern, f): 
#            f_path = os.path.join(ninjaoutDir, f)
#            try:
#                if os.path.isfile(f_path):
#                    zip_ref.write(f_path, basename(f_path))
#            except Exception as e:
#                print(e)
#    pattern = ".prj"
#    for f in os.listdir(ninjaoutDir):
#        if re.search(pattern, f): 
#            f_path = os.path.join(ninjaoutDir, f)
#            try:
#                if os.path.isfile(f_path):
#                    zip_ref.write(f_path, basename(f_path))
#            except Exception as e:
#                print(e)
#    pattern = ".shx"
#    for f in os.listdir(ninjaoutDir):
#        if re.search(pattern, f): 
#            f_path = os.path.join(ninjaoutDir, f)
#            try:
#                if os.path.isfile(f_path):
#                    zip_ref.write(f_path, basename(f_path))
#            except Exception as e:
#                print(e)
#    pattern = ".dbf"
#    for f in os.listdir(ninjaoutDir):
#        if re.search(pattern, f): 
#            f_path = os.path.join(ninjaoutDir, f)
#            try:
#                if os.path.isfile(f_path):
#                    zip_ref.write(f_path, basename(f_path))
#            except Exception as e:
#                print(e)
#zip_ref.close()
