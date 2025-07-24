#!/usr/bin/env python3

import subprocess
import sys
import shutil
import os
from os.path import basename
import re
import zipfile

import datetime
import urllib

import json

def usage():
    print("Not enough args!!!\n")
    print("Usage:\n")
    print("copyFiles path/to/config.json\n")

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
ninjaoutDir = config['paths']['ninjaoutDir']
serverDir = config['paths']['serverDir']

print("scp %swrf*.kml %s" % (ninjaoutDir, serverDir))

#copy the WRF kml files
#p = subprocess.Popen(["scp -i /home/natalie/.ssh/id_ed25519 %swrf*.kml %s" % (ninjaoutDir, serverDir)], cwd = nightly_wrf, shell = True, stdout=subprocess.PIPE)
#out, err = p.communicate()

#copy the WRF legend files
#p = subprocess.Popen(["scp -i /home/natalie/.ssh/id_ed25519 %s*.bmp %s" % (ninjaoutDir, serverDir)], cwd = nightly_wrf, shell = True, stdout=subprocess.PIPE)
#out, err = p.communicate()

#copy the WRF legend files
#p = subprocess.Popen(["scp -i /home/natalie/.ssh/id_ed25519 %swxLog.txt %s" % (ninjaoutDir, serverDir)], cwd = nightly_wrf, shell = True, stdout=subprocess.PIPE)
#out, err = p.communicate()

#copy the zipped output files for download from the hires-wrf webpage
p = subprocess.Popen(["scp -i /home/natalie/.ssh/id_ed25519 %swrf.zip %s" % (ninjaoutDir, serverDir)], cwd = nightly_wrf, shell = True, stdout=subprocess.PIPE)
out, err = p.communicate()

#copy the wrfout file
p = subprocess.Popen(["scp -i /home/natalie/.ssh/id_ed25519 %s../wrfout.nc %s" % (ninjaoutDir, serverDir)], cwd = nightly_wrf, shell = True, stdout=subprocess.PIPE)
out, err = p.communicate()

