#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt
from netCDF4 import Dataset
from wrf import getvar, to_np
import math
import cartopy.crs as ccrs
import os

# ----------------------------
# Open file
# ----------------------------
ncfile = Dataset("/home/natalie/carr/wrf/output/d02_more_vertical_layers/wrfout_d02_2018-07-26_070000.nc")

timeidx = 19

# ----------------------------
# Get variables
# ----------------------------
u = getvar(ncfile, "ua", timeidx=timeidx)
v = getvar(ncfile, "va", timeidx=timeidx)
w = getvar(ncfile, "wa", timeidx=timeidx)
z = getvar(ncfile, "z", timeidx=timeidx)

u = to_np(u)
v = to_np(v)
w = to_np(w)
z = to_np(z)

# ----------------------------
# Compute grid spacing
# ----------------------------
dz = np.diff(z, axis=0)

# expand last layer back to 3D
dz_last = dz[-1:,:,:]   # keeps shape (1, ny, nx)

dz = np.concatenate([dz, dz_last], axis=0)

# ----------------------------
# Derivatives
# ----------------------------
# horizontal derivatives (uniform grid)
dx = 333.0
dy = 333.0

dudy = np.gradient(u, dy, axis=1)
dvdx = np.gradient(v, dx, axis=2)

dwdx = np.gradient(w, dx, axis=2)
dwdy = np.gradient(w, dy, axis=1)

# vertical derivatives (non-uniform grid)
dudz = np.zeros_like(u)
dvdz = np.zeros_like(v)

dudz[1:-1,:,:] = (u[2:,:,:] - u[:-2,:,:]) / (z[2:,:,:] - z[:-2,:,:])
dvdz[1:-1,:,:] = (v[2:,:,:] - v[:-2,:,:]) / (z[2:,:,:] - z[:-2,:,:])

dudz[0,:,:]  = (u[1,:,:] - u[0,:,:]) / (z[1,:,:] - z[0,:,:])
dudz[-1,:,:] = (u[-1,:,:] - u[-2,:,:]) / (z[-1,:,:] - z[-2,:,:])

dvdz[0,:,:]  = (v[1,:,:] - v[0,:,:]) / (z[1,:,:] - z[0,:,:])
dvdz[-1,:,:] = (v[-1,:,:] - v[-2,:,:]) / (z[-1,:,:] - z[-2,:,:])

# ----------------------------
# Horizontal vorticity
# ----------------------------
omega_x = dwdy - dvdz
omega_y = dudz - dwdx

omega_h = np.sqrt(omega_x**2 + omega_y**2)

# ----------------------------
# Plot a horizontal slice (e.g., level 10)
# ----------------------------
level = 4

plt.figure(figsize=(10,6))


from wrf import latlon_coords

lats, lons = latlon_coords(getvar(ncfile, "ua", timeidx=timeidx))
lats = to_np(lats)
lons = to_np(lons)

plt.contourf(lons, lats, omega_h[level,:,:], levels=30, cmap="RdBu_r")
plt.colorbar(label="Horizontal Vorticity (s⁻¹)")
plt.title(f"Horizontal Vorticity Magnitude (level {level})")

center_lat = 40.60998
center_lon = -122.432530
bearing_deg = 320.0
transect_half_length_km = 35

R = 6371.0

lat1 = math.radians(center_lat)
lon1 = math.radians(center_lon)
bearing_rad = math.radians(bearing_deg)
d = transect_half_length_km / R

# Forward endpoint
lat2 = math.asin(math.sin(lat1)*math.cos(d) +
            math.cos(lat1)*math.sin(d)*math.cos(bearing_rad))

lon2 = lon1 + math.atan2(math.sin(bearing_rad)*math.sin(d)*math.cos(lat1),
            math.cos(d)-math.sin(lat1)*math.sin(lat2))

# Reverse endpoint
bearing_rev = math.radians((bearing_deg + 180) % 360)

lat3 = math.asin(math.sin(lat1)*math.cos(d) +
            math.cos(lat1)*math.sin(d)*math.cos(bearing_rev))

lon3 = lon1 + math.atan2(math.sin(bearing_rev)*math.sin(d)*math.cos(lat1),
            math.cos(d)-math.sin(lat1)*math.sin(lat3))

lat2, lon2 = math.degrees(lat2), math.degrees(lon2)
lat3, lon3 = math.degrees(lat3), math.degrees(lon3)

# Plot transect
plt.plot([lon2, lon3], [lat2, lat3],
            color='magenta', linewidth=3, label="320° Transect")

plt.plot(center_lon, center_lat,
    marker='*',
    markersize=18,
    markerfacecolor='black',
    markeredgecolor='white',
    markeredgewidth=2,
    label="Fire Whirl")

plt.text(center_lon + 0.02, center_lat + 0.02,
    "Fire Whirl",
    color='white',
    fontsize=12,
    bbox=dict(facecolor='black', edgecolor='white', boxstyle='round'))



plt.show()

