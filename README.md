# hires-wrf
High-resolution WRF simulations for wildland fire

This code provides workflows for:

* Automated 1-km runs downscaled from 3-km HRRR forecasts (see `src/autorun_forecast/runMultipleDomains.py`)

  WRF is initialized with 3-km HRRR every morning at 0400 LT and downscaled to 1 km horizontal resolution. The 10-m wind field is posted online as a KMZ for 1200-2100 LT. The domains are positioned to support the needs of wildland fire managers, particularly IMETs, LTANs, and FBANs assigned to active incidents.
  The 1-km WRF is further downscaled with WindNinja.
  
  Output available at: [https://ninjastorm.firelab.org/hires_wrf/](https://ninjastorm.firelab.org/hires_wrf/)

* On-demand 1-km runs downscaled from 3-km HRRR forecasts (see `src/on_demand_forecast/hiresWRF.py`)
  
  Note that `fetchHRRR` must be run independently before `hiresWRF.py` is called

* PastCast simluations (see `src/pastcast/`)
