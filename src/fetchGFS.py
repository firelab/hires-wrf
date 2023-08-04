#!/usr/bin/env python

import datetime
import subprocess

# Fetches all 18 timesteps in forecast initialized on the current day at 1000 UTC (0400 MDT)

dataDir = '/media/natalie/ExtraDrive2/nightly_wrf/data/'

#MODIFIED FOR NEW ZEALAND
#grab 12 UTC forecast starting with f=006 at 1000 MDT (f000 in this forecast is for midnight NZST tomorrow, f006 is for 0800 NZST tomorrow)
date = datetime.datetime.now().strftime('%Y%m%d')
#New Zealand is 12 hr ahead of UTC
#date = datetime.datetime.utcnow()
#date = date - datetime.timedelta(days=1)
#date = date.strftime('%Y%m%d')

timeList = ['006', '007', '008', '009', '010', '011', '012', '013', '014']

#wget https://nomads.ncep.noaa.gov/pub/data/nccf/com/gfs/prod/gfs.20230425/12/atmos/gfs.t12z.pgrb2.0p25.f106

for time in timeList:
    print 'Downloading t12z.pgrb2.0p25.f%s' % time
    dataFile = 'http://nomads.ncep.noaa.gov/pub/data/nccf/com/gfs/prod/gfs.%s/12/atmos/gfs.t12z.pgrb2.0p25.f%s'\
                % (date, time)
    p = subprocess.Popen(["wget %s" % dataFile], cwd = dataDir, shell = True, stdout=subprocess.PIPE)
    out, err = p.communicate()

print 'Download complete!'
