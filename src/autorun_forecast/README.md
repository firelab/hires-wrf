# Steps to run with one or more domains
1. Edit `config.json` and put it in `${nightly_wrf}/output/d01/`. Repeat for additional domains as needed, putting each config.json in `${nightly_wrf}/output/d02`, `${nightly_wrf}/output/d03`, etc.

2. `runMultipleDomains.py` controls the runs. Comment out/add domains as needed. This script:
    - reads one or more config files from `${nightly_wrf}/output/d0*/config.json`
    - cleans up `${nightly_wrf}` from any previous runs 
    - runs `fetchHRRR.py`
    - runs `hiresWRF.py` on each domain  

3. `hiresWRF.py` does the following for each domain:
    - reads in the current config file for the domain
    - runs `runGeogrid.py`
    - runs `runUngrib.py`
    - runs `metgrid.exe`
    - runs `runReal.py`
    - runs `wrf.exe`
    - runs `runWindNinja.py`
    - runs `packageOutput.py`
    - runs `copyFiles.py`


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
