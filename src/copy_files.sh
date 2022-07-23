#! /bin/bash

#copy the WRF kml files
scp /media/natalie/ExtraDrive2/nightly_wrf/output/ninjaout/wrf*.kml ubuntu@192.168.59.7:/home/ubuntu/ninjaInput/wrfSim/wrf

#copy the WRF legend files
scp /media/natalie/ExtraDrive2/nightly_wrf/output/ninjaout/*.bmp ubuntu@192.168.59.7:/home/ubuntu/ninjaInput/wrfSim/wrf_key

#copy the WRF legend files
scp /media/natalie/ExtraDrive2/nightly_wrf/output/ninjaout/wxLog.txt ubuntu@192.168.59.7:/home/ubuntu/ninjaInput/wrfSim

#copy the WindNinja output files for download from the hires-wrf webpage
scp /media/natalie/ExtraDrive2/nightly_wrf/output/ninjaout/*.kmz ubuntu@192.168.59.7:/home/ubuntu/ninjaInput/wrfSim/ninjaout/1km_wrf
scp /media/natalie/ExtraDrive2/nightly_wrf/output/ninjaout/*.shp ubuntu@192.168.59.7:/home/ubuntu/ninjaInput/wrfSim/ninjaout/1km_wrf
scp /media/natalie/ExtraDrive2/nightly_wrf/output/ninjaout/*.shx ubuntu@192.168.59.7:/home/ubuntu/ninjaInput/wrfSim/ninjaout/1km_wrf
scp /media/natalie/ExtraDrive2/nightly_wrf/output/ninjaout/*.dbf ubuntu@192.168.59.7:/home/ubuntu/ninjaInput/wrfSim/ninjaout/1km_wrf
scp /media/natalie/ExtraDrive2/nightly_wrf/output/ninjaout/*.prj ubuntu@192.168.59.7:/home/ubuntu/ninjaInput/wrfSim/ninjaout/1km_wrf
scp /media/natalie/ExtraDrive2/nightly_wrf/output/ninjaout/*.asc ubuntu@192.168.59.7:/home/ubuntu/ninjaInput/wrfSim/ninjaout/1km_wrf

#copy the wrfout file
scp /media/natalie/ExtraDrive2/nightly_wrf/output/out.nc ubuntu@192.168.59.7:/home/ubuntu/ninjaInput/wrfSim/ninjaout/1km_wrf
