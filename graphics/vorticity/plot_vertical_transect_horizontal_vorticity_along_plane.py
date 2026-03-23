#!/usr/bin/env python3

import numpy as np
import math
import matplotlib.pyplot as plt
from netCDF4 import Dataset
from wrf import getvar, vertcross, CoordPair, to_np, interpline

# -----------------------------
# Open WRF output
# -----------------------------
ncfile = Dataset("/home/natalie/carr/wrf/output/d02_more_vertical_layers/wrfout_d02_2018-07-26_070000.nc")
time_index = 19

# -----------------------------
# Extract variables
# -----------------------------
u = getvar(ncfile, "ua", timeidx=time_index)
v = getvar(ncfile, "va", timeidx=time_index)
w = getvar(ncfile, "wa", timeidx=time_index)
z = getvar(ncfile, "z", timeidx=time_index)
zstag = getvar(ncfile, "zstag", timeidx=time_index)
terrain = getvar(ncfile, "ter")

# -----------------------------
# Define 320° transect
# -----------------------------
center_lat = 40.60998
center_lon = -122.432530
bearing_deg = 320.0
transect_half_length_km = 35

R = 6371.0  # Earth radius (km)
bearing_rad = math.radians(bearing_deg)
lat1 = math.radians(center_lat)
lon1 = math.radians(center_lon)
d = transect_half_length_km / R

# Forward endpoint
lat2 = math.asin(np.sin(lat1)*np.cos(d) + np.cos(lat1)*np.sin(d)*np.cos(bearing_rad))
lon2 = lon1 + np.arctan2(np.sin(bearing_rad)*np.sin(d)*np.cos(lat1),
                                 np.cos(d)-np.sin(lat1)*np.sin(lat2))
# Reverse endpoint
bearing_rev = math.radians((bearing_deg + 180) % 360)
lat3 = math.asin(np.sin(lat1)*np.cos(d) + np.cos(lat1)*np.sin(d)*np.cos(bearing_rev))
lon3 = lon1 + np.arctan2(np.sin(bearing_rev)*np.sin(d)*np.cos(lat1),
                                 np.cos(d)-np.sin(lat1)*np.sin(lat3))

start_point = CoordPair(lat=math.degrees(lat2), lon=math.degrees(lon2))
end_point   = CoordPair(lat=math.degrees(lat3), lon=math.degrees(lon3))

# -----------------------------
# Compute vertical cross sections
# -----------------------------
u_xsect = vertcross(u, z, wrfin=ncfile, start_point=start_point, end_point=end_point, latlon=True)
v_xsect = vertcross(v, z, wrfin=ncfile, start_point=start_point, end_point=end_point, latlon=True)
#z_xsect = vertcross(z, z, wrfin=ncfile, start_point=start_point, end_point=end_point, latlon=True)
z_xsect = vertcross(zstag, zstag, wrfin=ncfile, start_point=start_point, end_point=end_point, latlon=True)

terrain_vals = to_np(interpline(terrain, start_point=start_point, end_point=end_point, wrfin=ncfile, latlon=True))

# -----------------------------
# Convert to numpy arrays
# -----------------------------
u_np = to_np(u_xsect)
v_np = to_np(v_xsect)
z_np = to_np(z_xsect)

# -----------------------------
# Distance along transect
# -----------------------------
nx = u_np.shape[1]
distance_km = np.linspace(-transect_half_length_km, transect_half_length_km, nx)

# -----------------------------
# Compute horizontal vorticity (cross-section) components
# Only dv/dz and du/dz matter for horizontal vorticity
# -----------------------------
dz = np.gradient(z_np, axis=0)  # vertical spacing (m)
dvdz = np.gradient(v_np, axis=0) / dz
dudz = np.gradient(u_np, axis=0) / dz

omega_h = np.sqrt(dvdz**2 + dudz**2)  # horizontal vorticity magnitude

# -----------------------------
# Plot
# -----------------------------
X, Z = np.meshgrid(distance_km, z_np[:,0])  # x=distance, z=height (use full vertical for shading)

fig, ax = plt.subplots(figsize=(12,6))
cf = ax.contourf(X, z_np, omega_h, levels=30, cmap="jet", extend="max")
plt.colorbar(cf, ax=ax, label="Horizontal Vorticity (s⁻¹)")

# Terrain
ax.fill_between(distance_km, 0, terrain_vals, color="saddlebrown", alpha=0.5)

# Centerline
ax.axvline(0, color="black", linestyle="--", linewidth=2)

# Labels
ax.set_xlabel("Distance Along Transect (km)")
ax.set_ylabel("Height (m)")
ax.set_title("Horizontal Vorticity along 320° Transect")

ax.set_ylim(0, 5000)
plt.tight_layout()
plt.show()

