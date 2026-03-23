#!/usr/bin/env python3

import os
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
from netCDF4 import Dataset
from wrf import getvar, latlon_coords, to_np, destagger
import numpy as np
from cartopy.io.img_tiles import StadiaMapsTiles
import math
import matplotlib.ticker as mticker

#=== Stadia Maps API key ===

try:
    STADIA_MAPS_API_KEY = os.environ["STADIA_MAPS_API_KEY"]
except KeyError:
    print("STADIA_MAPS_API_KEY is not set.")
    STADIA_MAPS_API_KEY = None

#=== Path to WRF output file ===

ncfile = Dataset("/home/natalie/carr/wrf/output/d01_more_vertical_layers/wrfout_d01_2018-07-26_070000.nc")
#ncfile = Dataset("/home/natalie/carr/wrf/output/d02_more_vertical_layers/wrfout_d02_2018-07-26_070000.nc")

time_index = 20

#=== Get 10-m wind components (for vectors) ===

u10 = getvar(ncfile, "U10", timeidx=time_index)
v10 = getvar(ncfile, "V10", timeidx=time_index)

#=== Load TKE ===

tke_raw = ncfile.variables["TKE_PBL"][time_index,:,:,:]

#Destagger vertical dimension

tke = destagger(tke_raw, 0)

#Use lowest model level

tke_sfc = tke[0,:,:]

#=== Get lat/lon coordinates ===

lats, lons = latlon_coords(u10)

#=== Subsample for vector density ===

#skip = (slice(None, None, 5), slice(None, None, 5))
skip = (slice(None, None, 10), slice(None, None, 10))

#=== Use Stadia Maps basemap ===

tiler = StadiaMapsTiles(style="stamen_terrain", apikey=STADIA_MAPS_API_KEY)

#=== Set up the plot ===

plt.figure(figsize=(12, 10))
ax = plt.axes(projection=ccrs.PlateCarree())
ax.add_image(tiler, 8)

gl=ax.gridlines(draw_labels=True)
gl.top_labels=False
gl.right_labels=False
gl.bottom_labels=True
gl.left_labels=True
gl.xlabel_style = {'size': 20}
gl.ylabel_style = {'size': 20}
gl.yformatter = mticker.FormatStrFormatter('%.2f') 
gl.xformatter = mticker.FormatStrFormatter('%.2f') 

#=== Plot TKE shading ===

c = ax.pcolormesh(
        to_np(lons), to_np(lats), tke_sfc,
        cmap="jet",
        vmin=0, vmax=4,
        transform=ccrs.PlateCarree()
        )

#=== Add colorbar ===

cb = plt.colorbar(c, ax=ax, orientation="horizontal", shrink=0.7, pad=0.06)
cb.set_label("TKE (m² s⁻²)", fontsize=24)
cb.ax.tick_params(labelsize=24)

#=== Plot wind vectors ===

ax.quiver(
        to_np(lons[skip]), to_np(lats[skip]),
        to_np(u10[skip]), to_np(v10[skip]),
        scale=200, width=0.0025, headwidth=4,
        transform=ccrs.PlateCarree(),
        color="black"
        )

#--- Add 320° transect line ---

center_lat = 40.60998
center_lon = -122.432530
bearing_deg = 320.0
transect_half_length_km = 110
#transect_half_length_km = 35

R = 6371.0

lat1 = math.radians(center_lat)
lon1 = math.radians(center_lon)
bearing_rad = math.radians(bearing_deg)
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

lat2 = math.degrees(lat2)
lon2 = math.degrees(lon2)
lat3 = math.degrees(lat3)
lon3 = math.degrees(lon3)

ax.plot([lon2, lon3], [lat2, lat3],
        color='darkviolet', linewidth=4,
        transform=ccrs.PlateCarree())

#--- Fire whirl marker ---

proj = ccrs.PlateCarree()
whirl_lat, whirl_lon = 40.60998, -122.432530

ax.plot(whirl_lon, whirl_lat, marker='*',
        markerfacecolor='black',
        markeredgecolor='white',
        markeredgewidth=2.5,
        markersize=32,
        transform=proj)

ax.text(whirl_lon + 0.02, whirl_lat + 0.07, "fire whirl",
        bbox=dict(facecolor='black', edgecolor='white',
            linewidth=1.5, boxstyle='round,pad=0.3'),
        color='white', fontsize=32,
        transform=proj)

plt.tight_layout()
plt.show()
