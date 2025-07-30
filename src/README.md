
# There are three ways WRF simulations can be run
1. `auto_forecast`: Automated hourly forecasts initialiazed with HRRR for 1200-2300 on the current day 
    - mostly used for operational wind forecasting on wildland fire incidents

2. `on_demand_forecast`: Hourly forecasts initialized with HRRR going out as far as you want

3. `pastcast`: Hourly pastcasts initialized with HRRR 

# Setting up a run
- All runs are controlled by `runWRF.sh`
    - This script properly sets the environment (PATH, LD_LIBRARY_PATH, etc.) for running as a cron job
- See `auto_forecast`, `on_demand_forecast`, or `pastcast` for speicfics related to each type of simulation
