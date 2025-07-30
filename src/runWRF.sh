#!/bin/bash

export PATH=/home/natalie/src/wrf-python/wrf-env/bin:/home/natalie/src/wrf/wrf_dependencies/wrf_dependencies/netcdf/bin:/home/natalie/src/wrf/wrf_dependencies/wrf_dependencies/mpich/bin:$PATH
export LD_LIBRARY_PATH=/home/natalie/src/wrf/wrf_dependencies/wrf_dependencies/netcdf/lib/:/home/natalie/src/wrf/wrf_dependencies/wrf_dependencies/grib2/lib/:/opt/jasper-1.900.29/lib/:$LD_LIBRARY_PATH 

/home/natalie/hires_wrf/./runMultipleDomains.py /home/natalie/hires_wrf/output/d01/config.json 
