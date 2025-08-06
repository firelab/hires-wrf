#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt
from netCDF4 import Dataset
from wrf import (getvar, interplevel, vertcross, CoordPair, to_np, latlon_coords)

# Open the WRF output file
ncfile = Dataset("/home/natalie/carr/wrf/output/d01/wrfout_d01_2018-07-26_070000.nc")

# Extract variables
u = getvar(ncfile, "ua", timeidx=20)
v = getvar(ncfile, "va", timeidx=20)
z = getvar(ncfile, "z", timeidx=20)         # model height (3D)
wspd = getvar(ncfile, "wspd", timeidx=20)   # wind speed magnitude
theta = getvar(ncfile, "theta", timeidx=20) # potential temperature

# Get grid dimensions
nz, ny, nx = wspd.shape

# Get latitude and longitude coordinates
lats, lons = latlon_coords(wspd)

## Define the vertical transect along the center of domain
#center_j = ny // 2
#start_point = CoordPair(lat=to_np(lats[center_j, 0]), lon=to_np(lons[center_j, 0]))
#end_point   = CoordPair(lat=to_np(lats[center_j, -1]), lon=to_np(lons[center_j, -1]))

# find index of closest row to desired latitude
desired_lat = 40.577
lat_diff = abs(to_np(lats[:, 0]) - desired_lat)
closest_j = lat_diff.argmin()

# Define a cross section through the desired lat
start_lat = float(lats[closest_j, 0])
start_lon = float(lons[closest_j, 0])
end_lat   = float(lats[closest_j, -1])
end_lon   = float(lons[closest_j, -1])

start_point = CoordPair(lat=to_np(start_lat), lon=to_np(start_lon))
end_point   = CoordPair(lat=to_np(end_lat), lon=to_np(end_lon))


# Interpolate wind speed and potential temperature along the transect
wspd_xsect = vertcross(wspd, z, wrfin=ncfile,
                               start_point=start_point, end_point=end_point,
                                                      latlon=True, meta=True)

theta_xsect = vertcross(theta, z, wrfin=ncfile,
                                start_point=start_point, end_point=end_point,
                                                        latlon=True, meta=True)

# Plotting
fig, ax = plt.subplots(figsize=(12, 6))

# Horizontal axis: grid points along transect
x = np.arange(wspd_xsect.shape[-1])
z_vals = to_np(wspd_xsect.coords["vertical"])

# Wind speed color fill
c = ax.contourf(x, z_vals, to_np(wspd_xsect), levels=30, cmap="viridis")
plt.colorbar(c, ax=ax, label="Wind Speed (m/s)")

# Overlay θ contours
theta_levels = np.arange(270, 350, 2)
contours = ax.contour(x, z_vals, to_np(theta_xsect), levels=theta_levels, colors="white", linewidths=1)
ax.clabel(contours, inline=True, fontsize=8, fmt="%d K")

# Labels and title
ax.set_title("Vertical Cross Section of Wind Speed with θ Contours\n(West to East, through %f)" % desired_lat)
ax.set_xlabel("Grid Point Along Cross Section")
ax.set_ylabel("Height (m)")

# Limit y-axis to 0–5 km
ax.set_ylim(0, 5000)

plt.tight_layout()
plt.savefig("wind_vertical_transect_with_theta.png", dpi=300)
plt.show()

