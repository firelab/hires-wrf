#!/usr/bin/env python3

import subprocess
import datetime

WPS = '/home/natalie/src/wrf/WPS/'
dataDir = '/home/natalie/hires_wrf/data/'

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
p = subprocess.Popen(["export LD_LIBRARY_PATH=/home/natalie/src/wrf/wrf_dependencies/wrf_dependencies/grib2/lib:/opt/jasper-1.900.29/lib/:$LD_LIBRARY_PATH && ./ungrib.exe"], cwd = WPS, shell = True, stdout=subprocess.PIPE)
out, err = p.communicate()

