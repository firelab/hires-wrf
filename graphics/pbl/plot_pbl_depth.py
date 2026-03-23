#!/usr/bin/env python3

import xarray as xr
from netCDF4 import Dataset
from wrf import getvar, ll_to_xy
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime

# --- user inputs ---
wrf_file = "/home/natalie/deer_creek/wrfout_d01_2025-07-12_120000.nc"
target_lat = 38.481476
target_lon = -109.416118
# -------------------

# Open dataset
nc = Dataset(wrf_file)

# Get full time series of PBLH
pblh = getvar(nc, "PBLH", timeidx=None)  # time = first dimension

# Convert lat/lon to nearest-grid x,y
ij = ll_to_xy(nc, target_lat, target_lon)
i, j = int(ij[0]), int(ij[1])

# Extract time series at this point
pblh_ts = pblh[:, j, i].to_numpy()   # meters AGL

ds = xr.open_dataset('/home/natalie/deer_creek/wrfout_d01_2025-07-12_120000.nc')

# Extract WRF times as strings
times_str = ds['Times'].astype(str).values

# Convert to Python datetime objects
times_dt = np.array([datetime.fromisoformat(t) for t in times_str])

# Extract hour-of-day for x-axis
hours = np.array([t.hour for t in times_dt])
print(hours)

plt.figure(figsize=(10,5))
plt.plot(hours, pblh_ts, marker='o')
plt.xlabel("Time (hours)")
plt.ylabel("PBL Height (m)")
plt.title(f"PBL Height at {target_lat:.2f}, {target_lon:.2f}")
plt.grid(True)
plt.show()

