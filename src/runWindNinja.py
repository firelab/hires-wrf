#!/usr/bin/env python

import subprocess
import shutil
import os
import re
import datetime

nightly_wrf = '/media/natalie/ExtraDrive2/nightly_wrf/'
RUN = '/home/natalie/src/wrf/WRFV3/run/'
outDir = nightly_wrf + "output/"
ninjaoutDir = outDir + "ninjaout/"

start_year = datetime.date.today().year
start_month = datetime.date.today().month
start_day = datetime.date.today().day

#copy wrfout file to output directory
wrfoutSrc = RUN + ('wrfout_d01_%s-%02d-%02d_18:00:00' % (start_year, start_month, start_day))
wrfoutDst = nightly_wrf + 'output/wrfout.nc'  
shutil.copyfile(wrfoutSrc, wrfoutDst) 

p = subprocess.Popen(["/media/natalie/ExtraDrive2/nightly_wrf/./runWN.sh"], cwd = outDir, shell = True, stdout=subprocess.PIPE)
out, err = p.communicate()
print out
print err

if p.returncode != 0:
    print "WindNinja: non-zero return code!"
    print p.returncode

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
