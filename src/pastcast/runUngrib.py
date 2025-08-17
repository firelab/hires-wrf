#!/usr/bin/env python3

import subprocess
import datetime
import json
import sys

def usage():
    print("Not enough args!!!\n")
    print("Usage:\n")
    print("runUngrib path/to/config.json\n")

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

WPS = config['paths']['wpsDir']
dataDir = config['paths']['dataDir']

print("WPS=%s" % WPS)
print("dataDir=%s" % dataDir)

#=============================================================================
#        Link to wx data
#=============================================================================
p = subprocess.Popen(["./link_grib.csh %s" % dataDir], cwd = WPS, shell = True, stdout=subprocess.PIPE)
out, err = p.communicate()

p = subprocess.Popen(["ln -sf ungrib/Variable_Tables/Vtable.HRRR Vtable"],
    cwd = WPS, shell = True, stdout=subprocess.PIPE)
out, err = p.communicate()

#=============================================================================
#        Run ungrib.exe
#=============================================================================
#p = subprocess.Popen(["./ungrib.exe", ">&", "log.ungrib"], cwd = WPS, shell = True, stdout=subprocess.PIPE)
p = subprocess.Popen(["export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/opt/jasper-1.900.29/lib/ && ./ungrib.exe"], cwd = WPS, shell = True, stdout=subprocess.PIPE)
out, err = p.communicate()

