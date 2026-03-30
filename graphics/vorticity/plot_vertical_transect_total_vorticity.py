#!/usr/bin/env python3

import numpy as np
import math
import matplotlib.pyplot as plt
from netCDF4 import Dataset
from wrf import (getvar, vertcross, CoordPair, to_np, interpline)

# --------------------------------------------------
# Open WRF file
# --------------------------------------------------
ncfile = Dataset("/home/natalie/carr/wrf/output/d02_more_vertical_layers/wrfout_d02_2018-07-26_070000.nc")

time_index = 19

# --------------------------------------------------
# Get variables
# --------------------------------------------------
u = to_np(getvar(ncfile, "ua", timeidx=time_index))
v = to_np(getvar(ncfile, "va", timeidx=time_index))
w = to_np(getvar(ncfile, "wa", timeidx=time_index))
z = to_np(getvar(ncfile, "z", timeidx=time_index))

theta = getvar(ncfile, "theta", timeidx=time_index)
terrain = getvar(ncfile, "ter")

# --------------------------------------------------
# Grid spacing
# --------------------------------------------------
dx = 333.0
dy = 333.0

# ============================================================
# === DERIVATIVES ============================================
# ============================================================

# --- Horizontal derivatives ---
dudy = np.gradient(u, dy, axis=1)
dudx = np.gradient(u, dx, axis=2)

dvdy = np.gradient(v, dy, axis=1)
dvdx = np.gradient(v, dx, axis=2)

dwdy = np.gradient(w, dy, axis=1)
dwdx = np.gradient(w, dx, axis=2)

# --- Vertical derivative (height-based, non-uniform grid) ---
def vertical_gradient(var, z):
    dvar_dz = np.empty_like(var)

    # Centered differences
    dvar_dz[1:-1,:,:] = (
        (var[2:,:,:] - var[:-2,:,:]) /
        (z[2:,:,:] - z[:-2,:,:])
    )

    # Bottom level (forward)
    dvar_dz[0,:,:] = (
        (var[1,:,:] - var[0,:,:]) /
        (z[1,:,:] - z[0,:,:])
    )

    # Top level (backward)
    dvar_dz[-1,:,:] = (
        (var[-1,:,:] - var[-2,:,:]) /
        (z[-1,:,:] - z[-2,:,:])
    )

    return dvar_dz

dudz = vertical_gradient(u, z)
dvdz = vertical_gradient(v, z)
dwdz = vertical_gradient(w, z)

# --------------------------------------------------
# Vorticity components
# --------------------------------------------------
omega_x = dwdy - dvdz
omega_y = dudz - dwdx
omega_z = dvdx - dudy

# --------------------------------------------------
# Total vorticity magnitude
# --------------------------------------------------
omega_mag = np.sqrt(omega_x**2 + omega_y**2 + omega_z**2)

# --------------------------------------------------
# Define transect
# --------------------------------------------------
center_lat = 40.60998
center_lon = -122.432530
bearing_deg = 320.0
transect_half_length_km = 35

R = 6371.0
bearing_rad = math.radians(bearing_deg)

lat1 = math.radians(center_lat)
lon1 = math.radians(center_lon)
d = transect_half_length_km / R

lat2 = math.asin(math.sin(lat1)*math.cos(d) +
math.cos(lat1)*math.sin(d)*math.cos(bearing_rad))

lon2 = lon1 + math.atan2(math.sin(bearing_rad)*math.sin(d)*math.cos(lat1),
math.cos(d)-math.sin(lat1)*math.sin(lat2))

bearing_rev = math.radians((bearing_deg + 180) % 360)

lat3 = math.asin(math.sin(lat1)*math.cos(d) +
math.cos(lat1)*math.sin(d)*math.cos(bearing_rev))

lon3 = lon1 + math.atan2(math.sin(bearing_rev)*math.sin(d)*math.cos(lat1),
math.cos(d)-math.sin(lat1)*math.sin(lat3))

start_point = CoordPair(lat=math.degrees(lat2), lon=math.degrees(lon2))
end_point   = CoordPair(lat=math.degrees(lat3), lon=math.degrees(lon3))

# --------------------------------------------------
# Cross sections
# --------------------------------------------------
omega_xsect = vertcross(omega_mag, z,
wrfin=ncfile,
start_point=start_point,
end_point=end_point,
latlon=False)

theta_xsect = vertcross(theta, z,
wrfin=ncfile,
start_point=start_point,
end_point=end_point,
latlon=False)

w_xsect = vertcross(w, z,
wrfin=ncfile,
start_point=start_point,
end_point=end_point,
latlon=False)

terrain_line = to_np(interpline(
terrain,
wrfin=ncfile,
start_point=start_point,
end_point=end_point
))

# --------------------------------------------------
# Coordinates
# --------------------------------------------------
num_points = omega_xsect.shape[-1]

distance_km = np.linspace(-transect_half_length_km,
transect_half_length_km,
num_points)

z_xsect = vertcross(z, z,
wrfin=ncfile,
start_point=start_point,
end_point=end_point,
latlon=False)

z_plot = to_np(z_xsect)

X = np.tile(distance_km, (z_plot.shape[0], 1))
Z = z_plot

# --------------------------------------------------
# Plot
# --------------------------------------------------
fig, ax = plt.subplots(figsize=(12,6))

omega_plot = to_np(omega_xsect)

cf = ax.contourf(
X,
Z,
omega_plot,
levels=np.linspace(0, 0.02, 41),
cmap="jet",
extend="max"
)

plt.colorbar(cf, ax=ax, label="Total Vorticity Magnitude (s⁻¹)")

# Theta contours
theta_levels = np.arange(280, 340, 1)
cs = ax.contour(X, Z, to_np(theta_xsect),
levels=theta_levels, colors="black", linewidths=1)
ax.clabel(cs, inline=True, fontsize=8)

# Vertical velocity
w_levels = np.arange(0.1, 1, 0.2)
ax.contour(X, Z, to_np(w_xsect),
levels=w_levels, colors="green", linewidths=1)

# Terrain
ax.fill_between(distance_km, 0, terrain_line,
color="saddlebrown", alpha=0.5)

ax.axvline(0, color="black", linestyle="--", linewidth=2)

# Labels
ax.set_title("Vertical Cross Section (320°)\nTotal Vorticity Magnitude, θ, and w")
ax.set_xlabel("Distance Along Transect (km)")
ax.set_ylabel("Height (m)")
ax.set_ylim(0, 5000)

plt.tight_layout()
plt.show()
