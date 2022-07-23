#! /bin/bash

#copy the WRF kml files
scp /media/natalie/ExtraDrive2/nightly_wrf/output/ninjaout/wrf*.kml natalie@fwas.usfs-i2.umt.edu:/home/natalie/nightly_wrf

#copy the WRF legend files
scp /media/natalie/ExtraDrive2/nightly_wrf/output/ninjaout/*.bmp natalie@fwas.usfs-i2.umt.edu:/home/natalie/nightly_wrf

#copy the WRF legend files
scp /media/natalie/ExtraDrive2/nightly_wrf/output/ninjaout/wxLog.txt natalie@fwas.usfs-i2.umt.edu:/home/natalie/nightly_wrf

#copy the WindNinja output files for download from the hires-wrf webpage
scp /media/natalie/ExtraDrive2/nightly_wrf/output/ninjaout/*.kmz natalie@fwas.usfs-i2.umt.edu:/home/natalie/nightly_wrf/ninjaout
scp /media/natalie/ExtraDrive2/nightly_wrf/output/ninjaout/*.shp natalie@fwas.usfs-i2.umt.edu:/home/natalie/nightly_wrf/ninjaout
scp /media/natalie/ExtraDrive2/nightly_wrf/output/ninjaout/*.shx natalie@fwas.usfs-i2.umt.edu:/home/natalie/nightly_wrf/ninjaout
scp /media/natalie/ExtraDrive2/nightly_wrf/output/ninjaout/*.dbf natalie@fwas.usfs-i2.umt.edu:/home/natalie/nightly_wrf/ninjaout
scp /media/natalie/ExtraDrive2/nightly_wrf/output/ninjaout/*.prj natalie@fwas.usfs-i2.umt.edu:/home/natalie/nightly_wrf/ninjaout
