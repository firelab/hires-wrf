# hires-wrf
High-resolution WRF simulations for wildland fire

This code provides workflows for:

* Automated 1-km runs downscaled from 3-km HRRR forecasts (see `runMultipleDomains.py`)

  WRF is initialized with 3-km HRRR every morning at 0400 LT and downscaled to 1 km horizontal resolution. 10-m wind and 2-m temperature are posted online for 1200-2100 LT. Nearby weather stations can also be toggled on/off. The domain is positioned to support the needs of wildland fire managers, particularly IMETS and FBANS assigned to active incidents.

  Output viewable at: [https://ninjastorm.firelab.org/hires_wrf/](https://ninjastorm.firelab.org/hires_wrf/)

* On-demand 1-km runs downscaled from 3-km HRRR forecasts (see `hiresWRF.py`)
  
  Note that `fetchHRRR` must be run independently before `hiresWRF.py` is called

* PastCast simluations (see `pastCast/`)
