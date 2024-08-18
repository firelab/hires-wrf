# Directory Structure for Multiple Domains
```
output/
├── d01
│   ├── config.json
│   ├── lime.tif
│   ├── nightlyWRF.log
│   ├── ninjaout
│   ├── runWindNinja.log
│   ├── wrf_initialization.cfg
│   └── wrfout.nc
├── d02
│   ├── config.json
│   ├── middle_fork.tif
│   ├── nightlyWRF.log
│   ├── ninjaout
│   ├── runWindNinja.log
│   ├── wrf_initialization.cfg
│   └── wrfout.nc
└── d03
    ├── config.json
    ├── nightlyWRF.log
    ├── ninjaout
    ├── runWindNinja.log
    ├── snag.tif
    ├── wrf_initialization.cfg
    └── wrfout.nc
```
# Config File Content
```
{                                                                                                                                                                                                                                                                                                                                                                                                                                  
    "paths": {                                                                                                                                                                                                                                                                                                                                                                                                                     
        "nightly_wrf": "/home/natalie/hires_wrf/",                                                                                                                                                                                                                                                                                                                                                                                 
        "logfile": "/home/natalie/hires_wrf/output/d01/nightlyWRF.log",                                                                                                                                                                                                                                                                                                                                                            
        "WPS": "/home/natalie/src/wrf/WPS/",                                                                                                                                                                                                                                                                                                                                                                                       
        "RUN": "/home/natalie/src/wrf/WRF/run/",                                                                                                                                                                                                                                                                                                                                                                                   
        "dataDir": "/home/natalie/hires_wrf/data/",                                                                                                                                                                                                                                                                                                                                                                                
        "wpsDir": "/home/natalie/src/wrf/WPS/",                                                                                                                                                                                                                                                                                                                                                                                    
        "runDir": "/home/natalie/src/wrf/WRF/run/",                                                                                                                                                                                                                                                                                                                                                                                
        "outDir": "/home/natalie/hires_wrf/output/d01/",                                                                                                                                                                                                                                                                                                                                                                           
        "ninjaoutDir": "/home/natalie/hires_wrf/output/d01/ninjaout/",                                                                                                                                                                                                                                                                                                                                                             
        "serverDir": "natalie@ninjastorm.firelab.org:/home/natalie/wrf/d01/"                                                                                                                                                                                                                                                                                                                                                       
    },                                                                                                                                                                                                                                                                                                                                                                                                                             
    "location": {                                                                                                                                                                                                                                                                                                                                                                                                                  
        "lat": "45.012853",                                                                                                                                                                                                                                                                                                                                                                                                        
        "lon": "-116.780326"                                                                                                                                                                                                                                                                                                                                                                                                       
    }                                                                                                                                                                                                                                                                                                                                                                                                                              
}
```
# Example Full Directory Strucutre
```
├── cleanup.py
├── config.json
├── copyFiles.py
├── copy_files.sh
├── data
│   ├── hrrr.t06z.wrfprsf12.grib2
│   ├── hrrr.t06z.wrfprsf13.grib2
│   ├── hrrr.t06z.wrfprsf14.grib2
│   ├── hrrr.t06z.wrfprsf15.grib2
│   ├── hrrr.t06z.wrfprsf16.grib2
│   ├── hrrr.t06z.wrfprsf17.grib2
│   ├── hrrr.t06z.wrfprsf18.grib2
│   ├── hrrr.t06z.wrfprsf19.grib2
│   ├── hrrr.t06z.wrfprsf20.grib2
│   ├── hrrr.t06z.wrfprsf21.grib2
│   ├── hrrr.t06z.wrfprsf22.grib2
│   └── hrrr.t06z.wrfprsf23.grib2
├── fetchGFS.py
├── fetchHRRR.py
├── graphics
│   └── plot_wrfout.R
├── hiresWRF.py
├── nightlyWRF.log
├── nightlyWRF.py
├── output
│   ├── d01
│   │   ├── config.json
│   │   ├── lime.tif
│   │   ├── nightlyWRF.log
│   │   ├── ninjaout
│   │   ├── runWindNinja.log
│   │   ├── wrf_initialization.cfg
│   │   └── wrfout.nc
│   ├── d02
│   │   ├── config.json
│   │   ├── middle_fork.tif
│   │   ├── nightlyWRF.log
│   │   ├── ninjaout
│   │   ├── runWindNinja.log
│   │   ├── wrf_initialization.cfg
│   │   └── wrfout.nc
│   └── d03
│       ├── config.json
│       ├── nightlyWRF.log
│       ├── ninjaout
│       ├── runWindNinja.log
│       ├── snag.tif
│       ├── wrf_initialization.cfg
│       └── wrfout.nc
├── packageOutput.py
├── runGeogrid.py
├── runMultipleDomains.py
├── runReal.py
├── runUngrib.py
├── runUngrib.sh
├── runWindNinja.py
├── runWN.sh
├── Vtable.HRRR
├── Vtable.HRRR_2015
└── wrf_initialization.cfg
```
