#! /bin/bash

output_dir="/home/natalie/hires_wrf/output/ninjaout/"
server_dir="natalie@ninjastorm.firelab.org:/home/natalie/wrf"

#copy the WRF kml files
scp $output_dir/wrf*.kml $server_dir

#copy the WRF legend files
scp $output_dir/*.bmp $server_dir

#copy the WRF legend files
scp $output_dir/wxLog.txt $server_dir

#copy the zipped output files for download from the hires-wrf webpage
scp $output_dir/wrf.zip  $server_dir/download

#copy the wrfout file
scp $output_dir../*.nc  $server_dir
