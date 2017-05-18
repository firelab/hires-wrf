#!/usr/bin/env python

import subprocess
import shutil
import os
import re
import datetime

nightly_wrf = '/home/nwagenbrenner/nightly_wrf/'
RUN = '/home/nwagenbrenner/src/WRF/WRFV3/run/'
outDir = nightly_wrf + "output/"
ninjaoutDir = outDir + "ninjaout/"

start_year = datetime.date.today().year
start_month = datetime.date.today().month
start_day = datetime.date.today().day

#copy wrfout file to output directory
wrfoutSrc = RUN + ('wrfout_d01_%s-%02d-%s_19:00:00' % (start_year, start_month, start_day))
wrfoutDst = nightly_wrf + 'output/wrfout.nc'  
shutil.copyfile(wrfoutSrc, wrfoutDst) 

windninja = '/home/nwagenbrenner/src/windninja/build/src/cli/./WindNinja_cli '
cfg = nightly_wrf + 'output/wrf_initialization.cfg'

p = subprocess.Popen([windninja + cfg], shell = True, stdout=subprocess.PIPE)
out, err = p.communicate()

print out
print err

pattern = "WRF-SURFACE-"
for f in os.listdir(outDir):
    if re.search(pattern, f): 
        f_path = os.path.join(outDir, f)
        try:
            if os.path.isfile(f_path):
                shutil.move(f_path, ninjaoutDir)
        except Exception as e:
            print(e)

pattern = "NINJAFOAM_"
for f in os.listdir(outDir):
    if re.search(pattern, f): 
        f_path = os.path.join(outDir, f)
        try:
            shutil.rmtree(f_path)
        except Exception as e:
            print(e)
