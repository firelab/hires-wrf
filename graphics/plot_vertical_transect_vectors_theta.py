#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt
from netCDF4 import Dataset
from wrf import (getvar, vertcross, CoordPair, to_np, latlon_coords)

# Open the wrfout file
ncfile = Dataset("/home/natalie/carr/wrf/output/d01/wrfout_d01_2018-07-26_070000.nc")

# Extract required fields
u = getvar(ncfile, "ua", timeidx=20)   # u-component (z, y, x)
w = getvar(ncfile, "wa", timeidx=20)   # vertical wind (z, y, x)
z = getvar(ncfile, "z", timeidx=20)    # height (z, y, x)
theta = getvar(ncfile, "theta", timeidx=20)  # potential temperature (z, y, x)
wspd = getvar(ncfile, "wspd", timeidx=20)    # wind speed magnitude (z, y, x)

# Get lat/lon grid and domain size
lats, lons = latlon_coords(wspd)

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

# Interpolate data along the vertical cross section
wspd_xsect  = vertcross(wspd, z, wrfin=ncfile, start_point=start_point, end_point=end_point, latlon=True)
theta_xsect = vertcross(theta, z, wrfin=ncfile, start_point=start_point, end_point=end_point, latlon=True)
u_xsect     = vertcross(u, z, wrfin=ncfile, start_point=start_point, end_point=end_point, latlon=True)
w_xsect     = vertcross(w, z, wrfin=ncfile, start_point=start_point, end_point=end_point, latlon=True)

# Create coordinate arrays
x = np.arange(wspd_xsect.shape[-1])  # horizontal index (grid points)
z_vals = to_np(wspd_xsect.coords["vertical"])

# Create meshgrid for quiver plotting
X, Z = np.meshgrid(x, z_vals)

# Reduce vector density for clarity
step = 1  # plot every 5th point
X_q = X[::step, ::step]
Z_q = Z[::step, ::step]
U_q = to_np(u_xsect)[::step, ::step]
W_q = to_np(w_xsect)[::step, ::step]

# Begin plotting
fig, ax = plt.subplots(figsize=(12, 6))

# Plot wind speed shading
cf = ax.contourf(x, z_vals, to_np(wspd_xsect), levels=30, cmap="viridis")
plt.colorbar(cf, ax=ax, label="Wind Speed (m/s)")

# Add potential temperature contours
theta_levels = np.arange(280, 340, 2)
cs = ax.contour(x, z_vals, to_np(theta_xsect), levels=theta_levels, colors="white", linewidths=1)
ax.clabel(cs, inline=True, fontsize=8, fmt="%.0f K")

# Add wind vectors
ax.quiver(X_q, Z_q, U_q, W_q, color="black", scale=300)

# Labels and limits
ax.set_title("Vertical Cross Section\nWind Speed Shading, θ Contours, Wind Vectors")
ax.set_xlabel("Grid Point Along Cross Section")
ax.set_ylabel("Height (m)")
ax.set_ylim(0, 5000)  # limit to 5 km

plt.tight_layout()
plt.savefig("wind_transect_wind_vectors_theta.png", dpi=300)
plt.show()

