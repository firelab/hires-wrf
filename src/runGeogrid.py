#!/usr/bin/env python

import subprocess
import datetime

WPS = '/home/nwagenbrenner/src/WRF/WPS/'

#=============================================================================
#        Edit namelist.wps
#=============================================================================
namelistFile = WPS + "namelist.wps"
namelist = open(namelistFile, 'w')

startdate = datetime.datetime.utcnow().strftime('%Y-%m-%d')
enddate = (datetime.datetime.utcnow()+datetime.timedelta(hours=24)).strftime('%Y-%m-%d')

namelist.write("&share\n")
namelist.write("wrf_core = 'ARW',\n")
namelist.write("max_dom = 1,\n")
#set start/end date (going out 18 hours)
namelist.write("start_date = '%s_19:00:00',\n" % startdate)
namelist.write("end_date   = '%s_04:00:00',\n" % enddate)
namelist.write("interval_seconds = 3600\n")
namelist.write("io_form_geogrid = 2,\n")
namelist.write("/\n")
namelist.write("\n")
#currently set to MSO domain
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
namelist.write("ref_lat   =  46.88,\n")
namelist.write("ref_lon   = -113.99,\n")
namelist.write("truelat1  =  30.0,\n")
namelist.write("truelat2  =  60.0,\n")
namelist.write("stand_lon = -113.99,\n")
namelist.write("geog_data_path = '/home/nwagenbrenner/src/WRF/WPS_GEOG/WPS_GEOG'\n")
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
p = subprocess.Popen(["./geogrid.exe", ">&", "log.geogrid"], cwd = WPS, shell = True, stdout=subprocess.PIPE)
out, err = p.communicate()

