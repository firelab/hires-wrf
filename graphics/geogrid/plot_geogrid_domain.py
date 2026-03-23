#!/usr/bin/env python3

import os
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from netCDF4 import Dataset
from wrf import latlon_coords
from cartopy.io.img_tiles import StadiaMapsTiles

# --- Set your API key for Stadia Maps ---
try:
    STADIA_MAPS_API_KEY = os.environ["STADIA_MAPS_API_KEY"]
except KeyError:
    raise RuntimeError("Set STADIA_MAPS_API_KEY in your environment first.")

# --- List of geogrid files ---
geo_files = [
    "/home/natalie/src/wrf/WPS/geo_em.d01.nc",
    "/home/natalie/src/wrf/WPS/geo_em.d02.nc",
]

# --- Set up Stadia basemap ---
tiler = StadiaMapsTiles(style="stamen_terrain", apikey=STADIA_MAPS_API_KEY)
tiler_proj = tiler.crs

# --- Start figure ---
plt.figure(figsize=(10, 10))
ax = plt.axes(projection=ccrs.PlateCarree())

# Add background basemap
ax.add_image(tiler, 7)  # zoom level (adjust if needed)

# Loop through each domain
for i, geo_file in enumerate(geo_files, start=1):
    if not os.path.exists(geo_file):
        print(f"Warning: {geo_file} not found, skipping.")
        continue

    ncfile = Dataset(geo_file)

    # Directly extract lat/lon arrays
    lats = ncfile.variables["XLAT_M"][0, :, :]
    lons = ncfile.variables["XLONG_M"][0, :, :]

    # Domain extent
    lat_min, lat_max = lats.min(), lats.max()
    lon_min, lon_max = lons.min(), lons.max()

    # Plot rectangle outline for the domain
    ax.plot([lon_min, lon_max, lon_max, lon_min, lon_min],
            [lat_min, lat_min, lat_max, lat_max, lat_min],
            transform=ccrs.PlateCarree(),
            linewidth=2,
            label=f"d0{i}")

# Add features
ax.add_feature(cfeature.BORDERS, linestyle="--", linewidth=0.7)
ax.add_feature(cfeature.COASTLINE, linewidth=0.7)

plt.legend()
plt.title("WRF Geogrid Domain Extents")
plt.show()

