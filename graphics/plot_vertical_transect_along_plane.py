#!/usr/bin/env python3

import numpy as np
import math
import matplotlib.pyplot as plt
from netCDF4 import Dataset
from wrf import (getvar, vertcross, CoordPair, to_np, latlon_coords, interpline)

# Open the wrfout file
ncfile = Dataset("/home/natalie/carr/wrf/output/d01_more_vertical_layers/wrfout_d01_2018-07-26_070000.nc")
#ncfile = Dataset("/home/natalie/carr/wrf/output/d02_more_vertical_layers/wrfout_d02_2018-07-26_070000.nc")

# --------------------------------------------------
# Extract variables
# --------------------------------------------------
time_index = 20

u = getvar(ncfile, "ua", timeidx=time_index)
v = getvar(ncfile, "va", timeidx=time_index)
w = getvar(ncfile, "wa", timeidx=time_index)
z = getvar(ncfile, "z", timeidx=time_index)
theta = getvar(ncfile, "theta", timeidx=time_index)
wspd = getvar(ncfile, "wspd", timeidx=time_index)
terrain = getvar(ncfile, "ter")  # terrain height (m)

# --------------------------------------------------
# Define angled transect (320° through center point)
# --------------------------------------------------
center_lat = 40.608912            #fire whirl locaiton at 17:23 LT
center_lon = -122.436602
#center_lat = 40.60998
#center_lon = -122.432530
bearing_deg = 320.0
transect_half_length_km = 110

R = 6371.0  # Earth radius (km)

bearing_rad = math.radians(bearing_deg)
lat1 = math.radians(center_lat)
lon1 = math.radians(center_lon)
d = transect_half_length_km / R

# Forward direction
lat2 = math.asin(
    math.sin(lat1) * math.cos(d) +
    math.cos(lat1) * math.sin(d) * math.cos(bearing_rad)
    )

lon2 = lon1 + math.atan2(
    math.sin(bearing_rad) * math.sin(d) * math.cos(lat1),
    math.cos(d) - math.sin(lat1) * math.sin(lat2)
    )

# Reverse direction
bearing_rev_rad = math.radians((bearing_deg + 180) % 360)

lat3 = math.asin(
    math.sin(lat1) * math.cos(d) +
    math.cos(lat1) * math.sin(d) * math.cos(bearing_rev_rad)
    )

lon3 = lon1 + math.atan2(
    math.sin(bearing_rev_rad) * math.sin(d) * math.cos(lat1),
    math.cos(d) - math.sin(lat1) * math.sin(lat3)
    )

start_point = CoordPair(lat=math.degrees(lat2), lon=math.degrees(lon2))
end_point   = CoordPair(lat=math.degrees(lat3), lon=math.degrees(lon3))

# --------------------------------------------------
# Compute vertical cross sections
# --------------------------------------------------
u_xsect = vertcross(u, z, wrfin=ncfile,
    start_point=start_point,
    end_point=end_point,
    latlon=True)

v_xsect = vertcross(v, z, wrfin=ncfile,
    start_point=start_point,
    end_point=end_point,
    latlon=True)

w_xsect = 5*vertcross(w, z, wrfin=ncfile,
    start_point=start_point,
    end_point=end_point,
    latlon=True)

theta_xsect = vertcross(theta, z, wrfin=ncfile,
    start_point=start_point,
    end_point=end_point,
    latlon=True)

wspd_xsect = vertcross(wspd, z, wrfin=ncfile,
    start_point=start_point,
    end_point=end_point,
    latlon=True)

# Sample terrain along the transect
terrain_vals = interpline(terrain, start_point=start_point, end_point=end_point, wrfin=ncfile, latlon=True)
terrain_vals = to_np(terrain_vals)

# --------------------------------------------------
# Rotate winds into along-transect direction
# --------------------------------------------------
# Rotate winds along transect and correct 180° flip
along_xsect = - (to_np(u_xsect) * np.sin(bearing_rad) +
               to_np(v_xsect) * np.cos(bearing_rad))

# --------------------------------------------------
# Build horizontal distance axis (km)
# --------------------------------------------------
num_points = wspd_xsect.shape[-1]
distance_km = np.linspace(-transect_half_length_km,
                       transect_half_length_km,
                       num_points)

z_vals = to_np(wspd_xsect.coords["vertical"])

X, Z = np.meshgrid(distance_km, z_vals)

# Reduce vector density
x_step = 4
z_step = 1

X_q = X[::z_step, ::x_step]
Z_q = Z[::z_step, ::x_step]
U_q = along_xsect[::z_step, ::x_step]
W_q = to_np(w_xsect)[::z_step, ::x_step]

# --------------------------------------------------
# Plot
# --------------------------------------------------
fig, ax = plt.subplots(figsize=(12, 6))

cf = ax.contourf(distance_km, z_vals,
    to_np(wspd_xsect),
    levels=np.linspace(0, 16, 33),
    cmap="Spectral_r",
    vmin=0, vmax=15)

cbar = plt.colorbar(cf, ax=ax, label="Wind Speed (m/s)", orientation='horizontal', pad=0.20)
cbar.set_label(label="Wind Speed (m/s)", size=22)
cbar.ax.tick_params(labelsize=22)

theta_levels = np.arange(280, 340, 1)
cs = ax.contour(distance_km, z_vals,
    to_np(theta_xsect),
    levels=theta_levels,
    colors="black",
    linewidths=2.0)

labels = ax.clabel(cs, inline=True, fontsize=18, fmt="%.0f K")

for l in labels:
    l.set_fontweight('bold')

ax.quiver(X_q, Z_q, U_q, W_q,
    color="black",
    scale=300)

# Terrain shading (filled polygon)
ax.fill_between(distance_km, 0, terrain_vals, color="saddlebrown", alpha=0.5)

#ax.set_title("Vertical Cross Section (320° Transect)\nWind Speed, θ, and Along-Section Wind Vectors")
ax.set_xlabel("Distance Along Transect (km)", fontsize=22)
ax.set_ylabel("Height (m)", fontsize=22)
ax.set_ylim(0, 5000)
#ax.axvline(0, color="black", linestyle="--", linewidth=3)  # center point
ax.axvline(0, color="darkviolet", linewidth=3)  # center point
ax.tick_params(axis='x', labelsize=22)
ax.tick_params(axis='y', labelsize=22)

plt.tight_layout()

#plt.savefig("wind_transect_320deg.png", dpi=300)
plt.show()
