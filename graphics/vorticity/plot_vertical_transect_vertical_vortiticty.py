#!/usr/bin/env python3

import numpy as np
import math
import matplotlib.pyplot as plt
from netCDF4 import Dataset
from wrf import (getvar, vertcross, CoordPair, to_np, interpline)

def fill_below_surface(field):
    """Fill NaNs below terrain in vertical cross section"""
    field = np.array(field)

    for j in range(field.shape[1]):  # loop over horizontal points
        col = field[:, j]

    valid = np.where(~np.isnan(col))[0]
    if len(valid) > 0:
        first = valid[0]
        col[:first] = col[first]  # fill downward

    field[:, j] = col

    return field

# --------------------------------------------------
# Open WRF file
# --------------------------------------------------
ncfile = Dataset("/home/natalie/carr/wrf/output/d02_more_vertical_layers/wrfout_d02_2018-07-26_070000.nc")

time_index = 19

# --------------------------------------------------
# Get variables
# --------------------------------------------------
u = getvar(ncfile, "ua", timeidx=time_index)
v = getvar(ncfile, "va", timeidx=time_index)
w = getvar(ncfile, "wa", timeidx=time_index)
z = getvar(ncfile, "z", timeidx=time_index)
theta = getvar(ncfile, "theta", timeidx=time_index)
terrain = getvar(ncfile, "ter")

u = to_np(u)
v = to_np(v)
w = to_np(w)
z = to_np(z)

# --------------------------------------------------
# Compute vertical vorticity ζ = dv/dx - du/dy
# --------------------------------------------------
dx = 333.0
dy = 333.0

dvdx = np.gradient(v, dx, axis=2)
dudy = np.gradient(u, dy, axis=1)

zeta = dvdx - dudy   # vertical vorticity (s^-1)

# --------------------------------------------------
# Define 320° transect
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

# forward point
lat2 = math.asin(math.sin(lat1)*math.cos(d) +
                        math.cos(lat1)*math.sin(d)*math.cos(bearing_rad))

lon2 = lon1 + math.atan2(math.sin(bearing_rad)*math.sin(d)*math.cos(lat1),
                                 math.cos(d)-math.sin(lat1)*math.sin(lat2))

# reverse point
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
zeta_xsect = vertcross(zeta, z,
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

# Terrain
terrain_line = to_np(interpline(
        terrain,
            wrfin=ncfile,
                start_point=start_point,
                    end_point=end_point
                    ))

# --------------------------------------------------
# Build coordinates
# --------------------------------------------------
num_points = zeta_xsect.shape[-1]

distance_km = np.linspace(
            -transect_half_length_km,
                 transect_half_length_km,
                      num_points
                      )

# vertical coordinate from z cross section
z_xsect = vertcross(z, z,
            wrfin=ncfile,
                start_point=start_point,
                    end_point=end_point,
                        latlon=False)

z_plot = to_np(z_xsect)   # shape (nz, nx)

# --- Build 2D coordinate grids ---
X = np.tile(distance_km, (z_plot.shape[0], 1))   # shape (nz, nx)
Z = z_plot                                       # already (nz, nx)


# --------------------------------------------------
# Plot
# --------------------------------------------------
fig, ax = plt.subplots(figsize=(12,6))

#zeta_plot = fill_below_surface(to_np(zeta_xsect))
zeta_plot = np.ma.masked_invalid(to_np(zeta_xsect))


# --- Vertical vorticity shading ---
cf = ax.contourf(
    X,
    Z,
    zeta_plot,
    levels=np.linspace(-0.005, 0.005, 41),
    cmap="RdBu_r",
    extend="both"
)

plt.colorbar(cf, ax=ax, label="Vertical Vorticity (s⁻¹)")

# --- Potential temperature contours ---
theta_levels = np.arange(280, 340, 1)

cs = ax.contour(
    X,
    Z,
    to_np(theta_xsect),
    levels=theta_levels,
    colors="black",
    linewidths=1
    )

ax.clabel(cs, inline=True, fontsize=8)

# --- Vertical velocity contours (optional, helpful) ---
w_levels = np.arange(0.1, 1, .2)

ax.contour(
    X,
    Z,
    to_np(w_xsect),
    levels=w_levels,
    colors="green",
    linewidths=1
    )

# --- Terrain ---
ax.fill_between(distance_km, 0, terrain_line,
                        color="saddlebrown", alpha=0.5)

# --- Center line ---
ax.axvline(0, color="black", linestyle="--", linewidth=2)

# --------------------------------------------------
# Labels
# --------------------------------------------------
ax.set_title("Vertical Cross Section (320°)\nVertical Vorticity, θ, and w")
ax.set_xlabel("Distance Along Transect (km)")
ax.set_ylabel("Height (m)")
ax.set_ylim(0, 5000)

plt.tight_layout()
plt.show()


