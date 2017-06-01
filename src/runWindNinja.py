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
wrfoutSrc = RUN + ('wrfout_d01_%s-%02d-%02d_18:00:00' % (start_year, start_month, start_day))
wrfoutDst = nightly_wrf + 'output/wrfout.nc'  
shutil.copyfile(wrfoutSrc, wrfoutDst) 

cfg = nightly_wrf + 'output/wrf_initialization.cfg'

p = subprocess.Popen(["WindNinja_cli " + cfg], cwd = outDir, shell = True, stdout=subprocess.PIPE)
out, err = p.communicate()
print out
print err

if p.returncode != 0:
    print "WindNinja: non-zero return code!"
    print p.returncode
    time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log.write('%s: WindNinja failed with return code %s \n' % (time, p.returncode))
    log.write("!!! Error during WindNinja !!!")
    log.close()
    sys.exit() #exit with return code 0

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
