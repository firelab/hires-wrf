#!/usr/bin/env python3

import subprocess
import datetime
import json
import sys
import os

def usage():
    print("Not enough args!!!\n")
    print("Usage:\n")
    print("fetchHRRR path/to/config.json\n")

if len(sys.argv) != 2:
    usage()
    sys.exit()

config_path = sys.argv[1]
print("The input config_path is: %s" % config_path)

#=============================================================================
#        Setup for current fetch
#=============================================================================
with open(config_path, 'r') as f:
    config = json.load(f)

dataDir = config['paths']['dataDir']
startYear = config['datetime']['startYear']
startMonth = config['datetime']['startMonth']
startDay = config['datetime']['startDay']
startHour = config['datetime']['startHour']
startMinute = config['datetime']['startMinute']
startSecond = config['datetime']['startSecond']
endYear = config['datetime']['endYear']
endMonth = config['datetime']['endMonth']
endDay = config['datetime']['endDay']
endHour = config['datetime']['endHour']
endMinute = config['datetime']['endMinute']
endSecond = config['datetime']['endSecond']

print("start datetime: %s-%s-%s-%s:%s:%s" % (startYear, startMonth, startDay, startHour, startMinute, startSecond))
print("end datetime: %s-%s-%s-%s:%s:%s" % (endYear, endMonth, endDay, endHour, endMinute, endSecond))

startStr = startYear+startMonth+startDay+startHour
endStr = endYear+endMonth+endDay+endHour

print("startStr = %s" % startStr)
print("endStr = %s" % endStr)

# Convert to datetime objects
startDt = datetime.datetime.strptime(startStr, '%Y%m%d%H')
endDt = datetime.datetime.strptime(endStr, '%Y%m%d%H')

# Generate list of datetimes
datetimeList = []
currentDt = startDt
while currentDt <= endDt:
    datetimeList.append(currentDt.strftime('%Y%m%d%H'))
    currentDt += datetime.timedelta(hours=1)

# Print result
print(datetimeList)

for datetime in datetimeList:
    dataFile = '\"gs://high-resolution-rapid-refresh/hrrr.%s/conus/hrrr.t%sz.wrfprsf00.grib2\"'\
            % (datetime[:8], datetime[-2:])
    print('Downloading %s' % dataFile)
    p = subprocess.Popen(["gsutil -m cp %s ." % dataFile], cwd = dataDir, shell = True, stdout=subprocess.PIPE)
    out, err = p.communicate()

    #prepend date to filenames 
    old_filename = 'hrrr.t%sz.wrfprsf00.grib2' % datetime[-2:] 
    old_path = os.path.join(dataDir, old_filename)
    new_filename = datetime[:8] + "." + old_filename 
    new_path = os.path.join(dataDir, new_filename)
    os.rename(old_path, new_path)
    print('renamed %s to %s' % (old_filename, new_filename))

print("Download complete!")


