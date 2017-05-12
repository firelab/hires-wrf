#!/usr/bin/env python

import datetime
import subprocess

# Fetches all 18 timesteps in forecast initialized on the current day at 1000 UTC (0400 MDT)

dataDir = '/home/nwagenbrenner/nightly_wrf/data'

date = datetime.datetime.now().strftime('%Y%m%d')

timeList = ['00', '01', '02', '03', '04', '05', '06', '07', '08', '09', '10',
            '11', '12', '13', '14', '15', '16', '17', '18']

for time in timeList:
    print 'Downloading t10z.wrfprsf%s.grib2' % time
    dataFile = 'http://nomads.ncep.noaa.gov/pub/data/nccf/com/hrrr/prod/hrrr.%s/hrrr.\
                t10z.wrfprsf%s.grib2' % (date, time)
    p = subprocess.Popen(["wget %s" % dataFile], cwd = dataDir, shell = True, stdout=subprocess.PIPE)
    out, err = p.communicate()

print 'Download complete!'
