#!/usr/bin/env python3

import xarray as xr
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import cartopy.io.img_tiles as cimgt
import os
import math
import textwrap

# --- Load the WRF WPS domain files ---
ds1 = xr.open_dataset("/home/natalie/src/wrf/WPS/geo_em.d01.nc")
ds2 = xr.open_dataset("/home/natalie/src/wrf/WPS/geo_em.d02.nc")

lat1, lon1, hgt1 = ds1['XLAT_M'][0], ds1['XLONG_M'][0], ds1['HGT_M'][0]
lat2, lon2 = ds2['XLAT_M'][0], ds2['XLONG_M'][0]

# --- Compute domain extent for plotting ---
lat_min = lat1.min().item() - 2.0
lat_max = lat1.max().item() + 2.0
lon_min = lon1.min().item() - 2.0
lon_max = lon1.max().item() + 2.0

# --- Define projection ---
proj = ccrs.PlateCarree()

# --- Create figure ---
fig = plt.figure(figsize=(12, 9))
ax = plt.axes(projection=proj)
ax.set_extent([lon_min, lon_max, lat_min, lat_max], crs=proj)

# --- Add Stadia Maps basemap ---
try:
        STADIA_MAPS_API_KEY = os.environ["STADIA_MAPS_API_KEY"]
except KeyError:
        raise ValueError("Set STADIA_MAPS_API_KEY in your environment.")

tiler = cimgt.StadiaMapsTiles(style="stamen_terrain", apikey=STADIA_MAPS_API_KEY)
ax.add_image(tiler, 8)  # zoom level

# --- Add map features ---
ax.coastlines()
ax.add_feature(cfeature.BORDERS)
ax.add_feature(cfeature.STATES, linewidth=0.5)

# --- Gridlines with labels only on left and bottom ---
gl = ax.gridlines(draw_labels=True)
gl.top_labels = False
gl.right_labels = False
gl.left_labels = True
gl.bottom_labels = True
gl.xlabel_style = {'size': 16}
gl.ylabel_style = {'size': 16}

# --- Plot terrain shading ---
terrain = ax.pcolormesh(lon1, lat1, hgt1, cmap='terrain', shading='auto', transform=proj)
cbar = plt.colorbar(terrain, ax=ax, orientation='vertical', pad=0.02, aspect=40)
cbar.ax.tick_params(labelsize=14)
cbar.set_label('Terrain Height (m)', fontsize=16)

# --- Function to draw domain boxes ---
#def plot_box(lat, lon, color, label):
#    ax.plot(lon[0, :], lat[0, :], color=color, linewidth=2)
#    ax.plot(lon[-1, :], lat[-1, :], color=color, linewidth=2)
#    ax.plot(lon[:, 0], lat[:, 0], color=color, linewidth=2)
#    ax.plot(lon[:, -1], lat[:, -1], color=color, linewidth=2)
#    # Move label slightly inside the box
#    ax.text(lon[0, 0]+0.05, lat[0, 0]+0.05, label, color=color, fontsize=14, weight='bold')
#    #ax.text(lon[0, 0]+0.05, lat[0, 0]+1.15, label, color=color, fontsize=14, weight='bold')

def plot_box(lat, lon, color, label):
    # Plot the domain box
    ax.plot(lon[0, :], lat[0, :], color=color, linewidth=2)   # top
    ax.plot(lon[-1, :], lat[-1, :], color=color, linewidth=2) # bottom
    ax.plot(lon[:, 0], lat[:, 0], color=color, linewidth=2)   # left
    ax.plot(lon[:, -1], lat[:, -1], color=color, linewidth=2) # right

    # Compute center of top edge
    top_lon = lon[0, :]
    top_lat = lat[0, :]
    center_lon = (top_lon.min() + top_lon.max()) / 2
    center_lat = top_lat.max()

    # Place label slightly above top edge
    ax.text(center_lon, center_lat + 0.2, label, 
    color=color, fontsize=16, weight='bold', ha='center', va='top')


# --- Plot domain boxes ---
plot_box(lat1, lon1, 'brown', 'd01')
plot_box(lat2, lon2, 'brown', 'd02')

# --- Add a custom point, e.g., Redding, CA ---
redding_lat, redding_lon = 40.5865, -122.3917
ax.plot(redding_lon, redding_lat, marker='.', color='black', markersize=14, transform=proj)
ax.text(redding_lon + 0.08, redding_lat + 0.05, "Redding", color='black', fontsize=16, weight='bold', transform=proj)

# --- Add a custom point, e.g., Eureka, CA ---
eureka_lat, eureka_lon = 40.8021, -124.1637
ax.plot(eureka_lon, eureka_lat, marker='.', color='black', markersize=14, transform=proj)
ax.text(eureka_lon - 0.75, eureka_lat + 0.05, "Eureka", color='black', fontsize=16, weight='bold', transform=proj)

# --- Add a custom label for Sacramento Valley ---
valley_lat, valley_lon = 39.40, -121.8917
ax.text(valley_lon, valley_lat, "Sacramento Valley", color='black', rotation=-55, 
        horizontalalignment='center', verticalalignment='center', fontsize=16, weight='bold', transform=proj)

# --- Add a custom label for Coast Range ---
ax.text(-123.4, 40.5, "Coast Range", color='black', rotation=-55, 
        horizontalalignment='center', verticalalignment='center', fontsize=16, weight='bold', transform=proj)

# --- Add a custom label for the Trinity Alps---
# Use textwrap.fill() to insert newlines at a specified width
wrapped_string = textwrap.fill("Trinity Alps", width=8) #
ax.text(-123.001822, 41.030432, wrapped_string, color='black', rotation=0, 
        horizontalalignment='center', verticalalignment='center', fontsize=16, weight='bold', transform=proj)

# --- Add 320° transect line ---
center_lat = 40.608912
center_lon = -122.436602
bearing_deg = 320.0
transect_half_length_km = 110

R = 6371.0  # Earth radius (km)

lat1 = math.radians(center_lat)
lon1 = math.radians(center_lon)
bearing_rad = math.radians(bearing_deg)
d = transect_half_length_km / R

# Forward endpoint
lat2 = math.asin(math.sin(lat1)*math.cos(d) +
    math.cos(lat1)*math.sin(d)*math.cos(bearing_rad))

lon2 = lon1 + math.atan2(math.sin(bearing_rad)*math.sin(d)*math.cos(lat1),
    math.cos(d)-math.sin(lat1)*math.sin(lat2))

# Reverse endpoint (bearing + 180°)
bearing_rev = math.radians((bearing_deg + 180) % 360)

lat3 = math.asin(math.sin(lat1)*math.cos(d) +
    math.cos(lat1)*math.sin(d)*math.cos(bearing_rev))

lon3 = lon1 + math.atan2(math.sin(bearing_rev)*math.sin(d)*math.cos(lat1),
    math.cos(d)-math.sin(lat1)*math.sin(lat3))

# Convert back to degrees
lat2 = math.degrees(lat2)
lon2 = math.degrees(lon2)
lat3 = math.degrees(lat3)
lon3 = math.degrees(lon3)

# Plot transect line
ax.plot([lon2, lon3], [lat2, lat3],
    color='brown', linewidth=2, linestyle="--",
    transform=ccrs.PlateCarree())

# --- Show plot ---
plt.show()

