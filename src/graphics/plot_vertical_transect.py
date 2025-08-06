#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt
from netCDF4 import Dataset
from wrf import getvar, interplevel, vertcross, CoordPair, to_np, get_basemap, latlon_coords, cartopy_xlim, cartopy_ylim

# Open the wrfout file
ncfile = Dataset("/home/natalie/carr/wrf/output/d01/wrfout_d01_2018-07-26_070000.nc")

# Extract wind components and height
u = getvar(ncfile, "ua", timeidx=20)   # u-component (staggered in x)
v = getvar(ncfile, "va", timeidx=20)   # v-component (staggered in y)
z = getvar(ncfile, "z", timeidx=20)    # model height

# Compute wind speed
wspd = getvar(ncfile, "wspd", timeidx=20)  # or compute from u, v: np.sqrt(u**2 + v**2)

# Get the grid shape
nz, ny, nx = wspd.shape

# Get lat/lon for full field
lats, lons = latlon_coords(wspd)

# Define a cross section line from west to east across the middle row
center_j = ny // 2  # middle of north-south domain
start_point = CoordPair(lat=to_np(lats[center_j, 0]), lon=to_np(lons[center_j, 0]))
end_point   = CoordPair(lat=to_np(lats[center_j, -1]), lon=to_np(lons[center_j, -1]))

# Interpolate the wind speed along this vertical cross section
wspd_xsect = vertcross(wspd, z, wrfin=ncfile, start_point=start_point, end_point=end_point,
                               latlon=True, meta=True)

# Plot the vertical cross section
fig, ax = plt.subplots(figsize=(12, 6))

x = np.arange(wspd_xsect.shape[-1])  # horizontal distance (grid points)
z_vals = to_np(wspd_xsect.coords["vertical"])  # height levels

c = ax.contourf(x, z_vals, to_np(wspd_xsect), levels=30, cmap="viridis")
plt.colorbar(c, ax=ax, label="Wind Speed (m/s)")

ax.set_title("Vertical Cross Section of Wind Speed (West to East, Center of Domain)")
ax.set_xlabel("Grid Point Along Cross Section")
ax.set_ylabel("Height (m)")

plt.tight_layout()
plt.savefig("wind_vertical_transect.png", dpi=300)
plt.show()

