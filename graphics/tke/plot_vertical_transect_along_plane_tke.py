#!/usr/bin/env python3

import numpy as np
import xarray as xr
import math
import matplotlib.pyplot as plt
from netCDF4 import Dataset
from wrf import (getvar, vertcross, CoordPair, to_np,
                         interpline, destagger)

# --------------------------------------------------
# Open the wrfout file
# --------------------------------------------------

ncfile = Dataset("/home/natalie/carr/wrf/output/d02_more_vertical_layers/wrfout_d02_2018-07-26_070000.nc")
#ncfile = Dataset("/home/natalie/carr/wrf/output/d01_more_vertical_layers/wrfout_d01_2018-07-26_070000.nc")

time_index = 20

# --------------------------------------------------
# Extract variables
# --------------------------------------------------

u = getvar(ncfile, "ua", timeidx=time_index)
v = getvar(ncfile, "va", timeidx=time_index)
w = getvar(ncfile, "wa", timeidx=time_index)
z = getvar(ncfile, "z", timeidx=time_index)

theta = getvar(ncfile, "theta", timeidx=time_index)
terrain = getvar(ncfile, "ter")

# --------------------------------------------------
# Load and destagger TKE with metadata
# --------------------------------------------------

tke_raw = ncfile.variables["TKE_PBL"][time_index,:,:,:]

# destagger vertically
tke_destag = destagger(tke_raw, 0)

# attach WRF coordinates using theta as template
tke = xr.DataArray(
    tke_destag,
    coords=theta.coords,
    dims=theta.dims,
    attrs={"description": "TKE_PBL"}
)

print("TKE raw shape:", tke_raw.shape)
print("z shape:", z.shape)
print("TKE destaggered shape:", tke.shape)

# --------------------------------------------------
# Define angled transect (320° through center point)
# --------------------------------------------------

center_lat = 40.60998
center_lon = -122.432530

bearing_deg = 320.0
transect_half_length_km = 35
#transect_half_length_km = 105

R = 6371.0

bearing_rad = math.radians(bearing_deg)

lat1 = math.radians(center_lat)
lon1 = math.radians(center_lon)

d = transect_half_length_km / R

# forward direction

lat2 = math.asin(
    math.sin(lat1) * math.cos(d) +
    math.cos(lat1) * math.sin(d) * math.cos(bearing_rad)
    )

lon2 = lon1 + math.atan2(
    math.sin(bearing_rad) * math.sin(d) * math.cos(lat1),
    math.cos(d) - math.sin(lat1) * math.sin(lat2)
    )

# reverse direction

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

u_xsect = vertcross(u, z,
    wrfin=ncfile,
    start_point=start_point,
    end_point=end_point,
    latlon=True)

v_xsect = vertcross(v, z,
    wrfin=ncfile,
    start_point=start_point,
    end_point=end_point,
    latlon=True)

w_xsect = 5 * vertcross(w, z,
    wrfin=ncfile,
    start_point=start_point,
    end_point=end_point,
    latlon=True)

theta_xsect = vertcross(theta, z,
    wrfin=ncfile,
    start_point=start_point,
    end_point=end_point,
    latlon=True)

tke_xsect = vertcross(tke, z,
    wrfin=ncfile,
    start_point=start_point,
    end_point=end_point,
    latlon=True)

# terrain profile

terrain_vals = to_np(interpline(terrain,
    start_point=start_point,
    end_point=end_point,
    wrfin=ncfile,
    latlon=True))

# --------------------------------------------------
# Rotate winds into along-transect direction
# --------------------------------------------------

along_xsect = -(
    to_np(u_xsect) * np.sin(bearing_rad) +
    to_np(v_xsect) * np.cos(bearing_rad)
    )

# --------------------------------------------------
# Build horizontal distance axis
# --------------------------------------------------

num_points = tke_xsect.shape[-1]

distance_km = np.linspace(-transect_half_length_km, transect_half_length_km, num_points)

# Check the coordinates
print(tke_xsect)

z_vals = to_np(tke_xsect.coords["vertical"])
tke_vals = to_np(tke_xsect)

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
fig, ax = plt.subplots(figsize=(12,6))

cf = ax.contourf(
    distance_km,
    z_vals,
    to_np(tke_xsect),
    levels=np.linspace(0,2.0,21),
    cmap="jet",
    extend="max"
)

plt.colorbar(cf, ax=ax, label="TKE (m² s⁻²)")

# theta contours
theta_levels = np.arange(280,340,1)

cs = ax.contour(
    distance_km,
    z_vals,
    to_np(theta_xsect),
    levels=theta_levels,
    colors="black",
    linewidths=1.2
    )

ax.clabel(cs, inline=True, fontsize=8, fmt="%.0f K")

# wind vectors
ax.quiver(
    X_q,
    Z_q,
    U_q,
    W_q,
    color="black",
    scale=300
    )

# terrain shading
ax.fill_between(
    distance_km,
    0,
    terrain_vals,
    color="saddlebrown",
    alpha=0.5
    )

ax.set_title("Vertical Cross Section (320° Transect)\nTKE, θ, and Along-Section Wind Vectors")

ax.set_xlabel("Distance Along Transect (km)")
ax.set_ylabel("Height (m)")

ax.set_ylim(0,5000)

# center point

ax.axvline(0, color="black", linestyle="--", linewidth=2)

plt.tight_layout()
plt.show()

