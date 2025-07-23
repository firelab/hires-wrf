#!/usr/bin/env python3

import subprocess
import datetime
import json
import sys

def usage():
    print("Not enough args!!!\n")
    print("Usage:\n")
    print("runGeogrid path/to/config.json\n")

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

wpsDir = config['paths']['wpsDir']
lat = config['location']['lat']
lon = config['location']['lon']
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

print("input lat: %s" % lat)
print("input lon: %s" % lon)

#=============================================================================
#        Edit namelist.wps
#=============================================================================
namelistFile = wpsDir + "namelist.wps"
namelist = open(namelistFile, 'w')

namelist.write("&share\n")
namelist.write("wrf_core = 'ARW',\n")
namelist.write("max_dom = 1,\n")
#set start/end date (going out 18 hours)
namelist.write("start_date = '%s-%s-%s_%s:%s:%s',\n" % (startYear, startMonth, startDay, startHour, startMinute, startSecond))
namelist.write("end_date   = '%s-%s-%s_%s:%s:%s',\n" % (endYear, endMonth, endDay, endHour, endMinute, endSecond))
namelist.write("interval_seconds = 3600\n")
namelist.write("io_form_geogrid = 2,\n")
namelist.write("/\n")
namelist.write("\n")
namelist.write("&geogrid\n")
namelist.write("parent_id         =   1,\n")
namelist.write("parent_grid_ratio =   1,\n") 
namelist.write("i_parent_start    =   1,\n")
namelist.write("j_parent_start    =   1,\n") 
namelist.write("e_we              =  100,\n") 
namelist.write("e_sn              =  100,\n") 
namelist.write("geog_data_res = 'default',\n")
namelist.write("dx = 1000,\n")
namelist.write("dy = 1000,\n")
namelist.write("map_proj = 'lambert',\n")
namelist.write("ref_lat   =  %s,\n" % lat)
namelist.write("ref_lon   = %s,\n" % lon)
namelist.write("truelat1  =  30.0,\n")
namelist.write("truelat2  =  60.0,\n")
namelist.write("stand_lon = %s,\n" % lon)
namelist.write("geog_data_path = '/home/natalie/src/wrf/WPS_GEOG'\n")
namelist.write("/\n")
namelist.write("\n")
namelist.write("&ungrib\n")
namelist.write("out_format = 'WPS',\n")
namelist.write("prefix = 'FILE',\n")
namelist.write("/\n")
namelist.write("\n")
namelist.write("&metgrid\n")
namelist.write("fg_name = 'FILE'\n")
namelist.write("io_form_metgrid = 2,\n") 
namelist.write("/\n")

namelist.close()

#=============================================================================
#        Run geogrid.exe
#=============================================================================
p = subprocess.Popen(["./geogrid.exe", ">&", "log.geogrid"], cwd = wpsDir, shell = True, stdout=subprocess.PIPE)
out, err = p.communicate()

