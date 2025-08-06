#!/usr/bin/env python3

import os
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from netCDF4 import Dataset
from wrf import getvar, latlon_coords, to_np, smooth2d
import numpy as np
from cartopy.io.img_tiles import StadiaMapsTiles
#help(StadiaMapsTiles)

try:
    STADIA_MAPS_API_KEY = os.environ["STADIA_MAPS_API_KEY"]
except KeyError:
    print("STADIA_MAPS_API_KEY is not set.")

# === Path to WRF output file ===
wrf_file = "/home/natalie/carr/wrf/output/d01/wrfout_d01_2018-07-26_070000.nc"
ncfile = Dataset(wrf_file)

# === Get 10-m wind components ===
u10 = getvar(ncfile, "U10")
v10 = getvar(ncfile, "V10")

# === Get lat/lon coordinates ===
lats, lons = latlon_coords(u10)

# === Subsample for vector density (adjust as needed) ===
skip = (slice(None, None, 2), slice(None, None, 2))  # every 10th point

# === Use Stadia Maps basemap ===
tiler = StadiaMapsTiles(style="stamen_terrain", apikey=STADIA_MAPS_API_KEY)  # Options: "outdoors", "alidade_smooth", etc.
tiler_proj = tiler.crs

# === Set up the plot ===
plt.figure(figsize=(12,10))
ax = plt.axes(projection=ccrs.PlateCarree())

ax.add_image(tiler, 8)  # Adjust zoom level as needed

# === Plot wind vectors ===
ax.quiver(to_np(lons[skip]), to_np(lats[skip]),
          to_np(u10[skip]), to_np(v10[skip]),
          scale=400, width=0.0025, headwidth=3)

# === Add title ===
plt.title("WRF 10-m Wind Vectors")

plt.tight_layout()
plt.show()

