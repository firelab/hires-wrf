#!/usr/bin/env python

import datetime
import subprocess

# 00/06/12/18 UTC cycles forecast out 36 hours, all other cycles go out 18 hours
# Fetches timesteps in forecast initialized 0600 UTC (midnight MDT)

dataDir = '/home/natalie/hires_wrf/data'

date = datetime.datetime.now().strftime('%Y%m%d')

#fetch noon through 2300
timeList = ['12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23']
#fetch 0600 tomorrow to 0600 the day after tomorrow
#timeList = ['24', '25', '26', '27', '28', '29', '30', '31', '32', '33', '34', '35', '36', '37', '38', '39', '40', '41', '42', '43', '44', '45', '46', '47', '48']
    #dataFile = 'http://nomads.ncep.noaa.gov/pub/data/nccf/com/hrrr/prod/hrrr.%s/conus/hrrr.t12z.wrfprsf%s.grib2'\

for time in timeList:
    print 'Downloading t06z.wrfprsf%s.grib2' % time
    dataFile = 'http://nomads.ncep.noaa.gov/pub/data/nccf/com/hrrr/prod/hrrr.%s/conus/hrrr.t06z.wrfprsf%s.grib2'\
                % (date, time)
    p = subprocess.Popen(["wget %s" % dataFile], cwd = dataDir, shell = True, stdout=subprocess.PIPE)
    out, err = p.communicate()

print("Download complete!")


##fetch noon through 2300
#timeList = ['06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16', '17']
#
#for time in timeList:
#    print 'Downloading t12.wrfprsf%s.grib2' % time
#    dataFile = 'http://nomads.ncep.noaa.gov/pub/data/nccf/com/hrrr/prod/hrrr.%s/conus/hrrr.t12z.wrfprsf%s.grib2'\
#                % (date, time)
#    p = subprocess.Popen(["wget %s" % dataFile], cwd = dataDir, shell = True, stdout=subprocess.PIPE)
#    out, err = p.communicate()
#
#print("Download complete!")
