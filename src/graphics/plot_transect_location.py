#!/usr/bin/env python3

import os
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
from cartopy.io.img_tiles import StadiaMapsTiles
from netCDF4 import Dataset
from wrf import getvar, latlon_coords, to_np

try:
    STADIA_MAPS_API_KEY = os.environ["STADIA_MAPS_API_KEY"]
except KeyError:
    print("STADIA_MAPS_API_KEY is not set.")

# Open WRF file
ncfile = Dataset("/home/natalie/carr/wrf/output/d01/wrfout_d01_2018-07-26_070000.nc")

# Get a 2D field to use for lat/lon (e.g., terrain height or surface pressure)
ter = getvar(ncfile, "ter")  # Terrain height
lats, lons = latlon_coords(ter)

# Calculate center row
ny, nx = lats.shape
center_j = ny // 2

# Start and end coordinates for the transect
start_lat = float(lats[center_j, 0])
start_lon = float(lons[center_j, 0])
end_lat   = float(lats[center_j, -1])
end_lon   = float(lons[center_j, -1])

# Set up basemap
tiler = StadiaMapsTiles(style="stamen_terrain", apikey=STADIA_MAPS_API_KEY)
crs = tiler.crs

fig = plt.figure(figsize=(10, 8))
ax = plt.axes(projection=crs)

# Set extent slightly larger than domain
min_lon = float(lons.min())
max_lon = float(lons.max())
min_lat = float(lats.min())
max_lat = float(lats.max())
ax.set_extent([min_lon, max_lon, min_lat, max_lat], crs=ccrs.PlateCarree())

# Add base map
ax.add_image(tiler, 8)

# Plot the transect line (center row)
ax.plot(
            [start_lon, end_lon],
                [start_lat, end_lat],
                    color="red", linewidth=2, marker="o", transform=ccrs.PlateCarree(),
                        label="Transect Line"
                        )

# Plot the domain outline
ax.plot(to_np(lons[0, :]), to_np(lats[0, :]), "k--", transform=ccrs.PlateCarree())  # top
ax.plot(to_np(lons[-1, :]), to_np(lats[-1, :]), "k--", transform=ccrs.PlateCarree())  # bottom
ax.plot(to_np(lons[:, 0]), to_np(lats[:, 0]), "k--", transform=ccrs.PlateCarree())  # left
ax.plot(to_np(lons[:, -1]), to_np(lats[:, -1]), "k--", transform=ccrs.PlateCarree())  # right

# Title and legend
ax.set_title("WRF Domain and Transect Location (Center Row)", fontsize=14)
ax.legend(loc="lower left")

plt.tight_layout()
plt.savefig("transect_location_map.png", dpi=300)
plt.show()

